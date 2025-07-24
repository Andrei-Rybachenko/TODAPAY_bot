from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_IDS
from db import get_content, update_content, reset_content
from keyboards.main import get_main_menu
router = Router()


class EditContent(StatesGroup):
    waiting_for_text = State()


@router.message(Command("admin"))
async def admin_entry(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("🚫 Access denied.")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Edit content", callback_data="edit_main")],
        [InlineKeyboardButton(text="📤 Export", callback_data="export_content")],
        [InlineKeyboardButton(text="♻️ Reset content", callback_data="reset_content")],
        [InlineKeyboardButton(text="🏠 Main menu", callback_data="back_to_user_menu")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close_admin")]
    ])

    await message.answer("🔧 Welcome to admin panel:", reply_markup=keyboard)


@router.callback_query(F.data == "reset_content")
async def handle_reset_content(callback: CallbackQuery):
    reset_content()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back to admin panel", callback_data="back_to_admin")]
        ]
    )
    await callback.message.edit_text("✅ Content reset to default.", reply_markup=keyboard)


@router.callback_query(F.data == "edit_main")
async def handle_edit_main(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 Who we are", callback_data="edit_who_we_are")],
        [InlineKeyboardButton(text="👥 Join our team", callback_data="edit_join_team")],
        [InlineKeyboardButton(text="🌐 Social media", callback_data="edit_social_media")],
        [InlineKeyboardButton(text="📞 Hot-line", callback_data="edit_hotline")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_admin")]
    ])
    await callback.message.edit_text("📝 Choose a section to edit:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("edit_"))
async def handle_section_choice(callback: CallbackQuery, state: FSMContext):
    section = callback.data.replace("edit_", "")

    if section not in ["who_we_are", "join_team", "social_media", "hotline"]:
        return await callback.answer("❌ Unknown section.")

    current = get_content(section)
    await state.update_data(section=section)
    await callback.message.edit_text(
        f"<b>Current content for <u>{section}</u>:</b>\n\n{current}\n\n"
        "✏️ Send new text to update this section."
    )
    await state.set_state(EditContent.waiting_for_text)


@router.message(EditContent.waiting_for_text)
async def save_new_text(message: Message, state: FSMContext):
    data = await state.get_data()
    section = data["section"]
    new_text = message.text

    update_content(section, new_text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back to admin panel", callback_data="back_to_admin")]
        ]
    )
    await message.answer(f"✅ <b>{section}</b> updated successfully.", reply_markup=keyboard)

    await state.clear()


@router.callback_query(F.data == "close_admin")
async def handle_close_admin(callback: CallbackQuery):
    await callback.message.edit_text("❌ Admin panel closed.")


@router.callback_query(F.data == "back_to_admin")
async def handle_back_to_admin(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Edit content", callback_data="edit_main")],
        [InlineKeyboardButton(text="📤 Export", callback_data="export_content")],
        [InlineKeyboardButton(text="♻️ Reset content", callback_data="reset_content")],
        [InlineKeyboardButton(text="🏠 Main menu", callback_data="back_to_user_menu")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close_admin")]
    ])

    await callback.message.edit_text("🔧 Back to admin panel:", reply_markup=keyboard)


@router.callback_query(F.data == "export_content")
async def handle_export_content(callback: CallbackQuery):
    from db import get_content

    sections = ["who_we_are", "join_team", "social_media", "hotline"]
    output = "📤 <b>Current content:</b>\n\n"

    for sec in sections:
        text = get_content(sec)
        output += f"<b>{sec}</b>:\n{text}\n\n{'-'*30}\n\n"

    await callback.message.edit_text(output[:4000])


@router.callback_query(F.data == "back_to_user_menu")
async def handle_back_to_user_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Choose a section below:",
        reply_markup=get_main_menu()
    )
