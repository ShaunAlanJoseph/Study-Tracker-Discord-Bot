from typing import Optional, List, Self, override, Dict

from discord import Interaction
from utils.context_manager import ctx_mgr
from utils.discord import send_message, get_files_from_message, BaseEmbed, BaseView
from utils.random import generate_random_string
from database import Database


class Flashcard:
    @classmethod
    def get_user_flashcards(cls, user_id: int) -> List[Self]:
        query = "SELECT card_id, user_id, question, options, answer, image FROM flashcard WHERE user_id = %s"
        results = Database.fetch_many(query, user_id)
        flashcards: List[Self] = []
        for result in results:
            flashcard = cls()
            flashcard.id = result[0]
            flashcard.author = result[1]
            flashcard.question = result[2]
            flashcard.options = result[3]
            flashcard.answer = result[4]
            flashcard.image = result[5]
            flashcards.append(flashcard)
        return flashcards
    
    def __init__(self):
        self.id: Optional[str] = None
        self.author: Optional[int] = None
        self.question: Optional[str] = None
        self.options: List[str] = []
        self.answer: Optional[str] = None
        self.image: Optional[bytes] = None

    def check_valid(self) -> bool:
        if not self.id or not self.author or not self.question or not self.answer:
            return False

        if (
            len(self.id) != 12
            or len(self.question) > 256
            or len(self.answer) > 256
            or len(self.options) == 1
            or len(self.options) > 8
        ):
            return False

        for option in self.options:
            if not option or len(option) > 256:
                return False

        return True

    def generate_id(self):
        while True:
            self.id = generate_random_string(12)
            try:
                query = f"SELECT card_id FROM flashcard WHERE card_id = '{self.id}'"
                Database.fetch_one(query)
            except:
                break

    def load_flashcard(self):
        assert self.id is not None
        query = f"SELECT user_id, question, options, answer, image FROM flashcard WHERE card_id = %s"
        try:
            result = Database.fetch_one(query, self.id)
        except ValueError:
            raise ValueError(f"Flashcard with id `{self.id}` not found.")

        self.author = result[0]
        self.question = result[1]
        self.options = result[2]
        self.answer = result[3]
        self.image = result[4]

    def save_flashcard(self):
        assert self.check_valid()
        query = f"INSERT INTO flashcard (card_id, user_id, question, options, answer, image) VALUES (%s, %s, %s, %s, %s, %s)"
        Database.execute_query(query, self.id, self.author, self.question, self.options, self.answer, self.image)

    def delete_flashcard(self):
        assert self.id is not None
        query = f"DELETE FROM flashcard WHERE card_id = %s"
        Database.execute_query(query, self.id)
    
    def get_details_embed(self) -> BaseEmbed:
        return FlashcardDetailsEmbed(self, show_answer=True, show_options=True)


class FlashcardDetailsEmbed(BaseEmbed):
    def __init__(self, flashcard: Flashcard, show_answer: bool, show_options: bool):
        super().__init__(title="Flashcard Details")
        self.add_field(name="ID", value=f"`{flashcard.id}`")
    
        assert flashcard.author is not None
        self.add_field(name="Author", value=f"<@{flashcard.author}>")

        assert flashcard.question is not None
        self.add_field(name="Question", value=flashcard.question)

        if show_options:
            for i, option in enumerate(flashcard.options):
                self.add_field(name=f"Option {i+1}", value=option)

        if show_answer:
            assert flashcard.answer is not None
            self.add_field(name="Answer", value=flashcard.answer)
    
        if flashcard.image is not None:
            self.set_image_from_bytes(flashcard.image, filename="card.png")


class FlashcardQuestionEmbed(BaseEmbed):
    def __init__(self, flashcard: Flashcard):
        assert flashcard.question is not None
        super().__init__(title=flashcard.question)

        if flashcard.image is not None:
            self.set_image_from_bytes(flashcard.image, filename="card.png")


class FlashcardAnswerEmbed(BaseEmbed):
    def __init__(self, flashcard: Flashcard, correct: bool):
        super().__init__(title="Correct!" if correct else "Incorrect!")

        assert flashcard.question is not None
        self.add_field(name="Question", value=flashcard.question)

        assert flashcard.answer is not None
        self.add_field(name="Answer", value=flashcard.answer)

        if flashcard.image is not None:
            self.set_image_from_bytes(flashcard.image, filename="card.png")


class FlashcardFlashView(BaseView):
    def __init__(self, flashcard: Flashcard):
        self.flashcard = flashcard

        self.show_answer: bool = False
        self.correct: bool = False
        super().__init__()
    
    def _add_items(self):
        if self.show_answer:
            self._add_button(label="Repeat", custom_id="repeat")
            
        else:
            options: Dict[str, str] = {}
            for i, option in enumerate(self.flashcard.options):
                options[f"{i}"] = option

            self._add_dropdown(custom_id="options", options=options, placeholder="Select an option")
    
    @override
    async def _button_clicked(self, interaction: Interaction, custom_id: str) -> None:
        await interaction.response.defer()

        if custom_id == "repeat":
            self.show_answer = False
        else:
            raise ValueError(f"Invalid custom_id: {custom_id}")

        await self.update_view()
    
    @override
    async def _dropdown_selected(self, *, interaction: Interaction, custom_id: str, values: List[str]) -> None:
        await interaction.response.defer()
        
        if custom_id == "options":
            self.correct = self.flashcard.options[int(values[0])] == self.flashcard.answer
            self.show_answer = True
        else:
            raise ValueError(f"Invalid custom_id: {custom_id}")
        
        await self.update_view()
    
    @override
    async def get_embed_files(self):
        if self.show_answer:
            embed = FlashcardAnswerEmbed(self.flashcard, correct=self.correct)
        else:
            embed = FlashcardQuestionEmbed(self.flashcard)
        return embed, None


class FlashcardListView(BaseView):
    @override
    @classmethod
    async def send_view(cls, flashcards: List[Flashcard]):
        view = cls(flashcards)
        await view.send()
    
    def __init__(self, flashcards: List[Flashcard]):
        self.flashcards = flashcards
        
        self.current_page = 0
        self.page_count = len(flashcards)
        super().__init__()
    
    def _add_items(self):
        self._add_button(label="⬅️", custom_id="previous", disabled=(self.current_page == 0))
        self._add_button(label="❌", custom_id="delete", disabled=(self.page_count == 0))
        self._add_button(label="➡️", custom_id="next", disabled=(self.current_page >= self.page_count - 1))
    
    @override
    async def _button_clicked(self, interaction: Interaction, custom_id: str) -> None:
        await interaction.response.defer()
        
        if custom_id == "previous":
            self.current_page -= 1
        elif custom_id == "next":
            self.current_page += 1
        elif custom_id == "delete":
            pass
        else:
            raise ValueError(f"Invalid custom_id: {custom_id}")
        
        await self.update_view()
    
    @override
    async def get_embed_files(self):
        if self.page_count == 0:
            return BaseEmbed(title="No Flashcards"), None
        
        embed = self.flashcards[self.current_page].get_details_embed()
        return embed, None


async def add_flashcard():
    message = ctx_mgr().get_init_context().message

    flashcard = Flashcard()

    # Setting the image
    files = await get_files_from_message(message)
    if len(files) > 1:
        await send_message(
            content="ERROR: Only one image is allowed.", mention_author=True
        )
        return
    if len(files) == 1:
        flashcard.image = list(files.values())[0].getvalue()
    
    # Setting the author
    flashcard.author = ctx_mgr().get_context_user_id()

    # Setting the id
    flashcard.generate_id()

    # Setting other details
    for line in message.content.splitlines():
        if line.startswith("# Q: "):
            flashcard.question = line[5:]
        elif line.startswith("## A: "):
            flashcard.answer = line[6:]
        elif line.startswith("- "):
            flashcard.options.append(line[2:])

    if not flashcard.check_valid():
        flashcard_format = (
            "# Q: <question 256 chars>"
            "## A: <answer 256 chars>\n"
            "- <option1 256 chars>\n"
            "- <option2 256 chars>\n"
            "- <option3>"
        )
        await send_message(
            content=f"ERROR: Invalid flashcard format.\nPlease use the following format:\n{flashcard_format}",
            mention_author=True,
        )
        return

    flashcard.save_flashcard()
    flashcard_embed = flashcard.get_details_embed()
    await send_message(embed=flashcard_embed)


async def list_flashcards():
    user_id = ctx_mgr().get_context_user_id()

    flashcards = Flashcard.get_user_flashcards(user_id)
    for flashcard in flashcards:
        print(f"DEBUG: Flashcard ID: {flashcard.id}")
    await FlashcardListView.send_view(flashcards)


async def flashcard_flash(card_id: str):
    flashcard = Flashcard()
    flashcard.id = card_id
    try:
        flashcard.load_flashcard()
    except ValueError as e:
        await send_message(content=str(e), mention_author=True)
        return
    view = FlashcardFlashView(flashcard)
    await view.send()

