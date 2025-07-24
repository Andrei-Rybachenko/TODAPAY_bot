from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from keyboards.main import get_main_menu
from google_sheets import save_user_to_sheet

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from google_sheets import save_resume_to_sheet

import datetime

from db import get_content


router = Router()


class ResumeForm(StatesGroup):
    waiting_for_email = State()
    waiting_for_message = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="▶️ Start", callback_data="start_button")]
        ]
    )
    await message.answer("Welcome! Press ▶️ Start to begin.", reply_markup=keyboard)


@router.callback_query(F.data == "start_button")
async def handle_start_button(callback: CallbackQuery):
    user = callback.from_user
    username = user.username or "no_username"
    user_id = user.id
    time = datetime.datetime.now().isoformat()

    save_user_to_sheet(username, user_id, time)

    await callback.message.edit_text(
        f"👋 Hello, <b>@{username}</b>!\nYou're now in the menu.",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "who_we_are")
async def handle_who_we_are(callback: CallbackQuery):
    text = get_content("who_we_are")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data == "back_to_menu")
async def handle_back(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Choose a section below:",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "join_team")
async def handle_join_team(callback: CallbackQuery):
    text = get_content("join_team")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📩 Send resume", callback_data="send_resume")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data == "send_resume")
async def start_resume(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📧 Please enter your email address:")
    await state.set_state(ResumeForm.waiting_for_email)


@router.message(ResumeForm.waiting_for_email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("💬 Now enter a short message or resume summary:")
    await state.set_state(ResumeForm.waiting_for_message)


@router.message(ResumeForm.waiting_for_message)
async def get_resume(message: Message, state: FSMContext):
    data = await state.get_data()
    email = data["email"]
    summary = message.text
    username = message.from_user.username or "no_username"
    user_id = message.from_user.id
    time = datetime.datetime.now().isoformat()

    save_resume_to_sheet(username, user_id, email, summary, time)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back to menu", callback_data="back_to_menu")]
        ]
    )
    await message.answer("✅ Thank you! We'll get in touch if opportunities appear.", reply_markup=keyboard)

    await state.clear()


@router.callback_query(F.data == "social_media")
async def handle_social_media(callback: CallbackQuery):
    text = get_content("social_media")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard, disable_web_page_preview=True)


@router.callback_query(F.data == "hotline")
async def handle_hotline(callback: CallbackQuery):
    text = get_content("hotline")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


def register_main_menu(dp):
    dp.include_router(router)

