import sqlite3

DB_NAME = "content.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS content (
            section TEXT PRIMARY KEY,
            text TEXT
        )
    """)
    # Заполним дефолтными данными при первом запуске
    defaults = {
        "who_we_are": (
            "<b>Who we are?</b>\n\n"
            "Founded in 2022, TODAPAY is built on a foundation of expertise in payment solutions, "
            "risk management, and financial operations. Our team has successfully developed fintech "
            "projects, facilitated international payments, and implemented alternative payment methods, "
            "ensuring businesses have access to secure, efficient, and scalable financial solutions.\n\n"
            "🌐 <a href='https://todapay.com/about-us'>More about us</a>"
        ),
        "join_team": (
            "<b>👥 Join our team</b>\n\n"
            "🌐 Career page: <a href='https://todapay.com/career'>todapay.com/career</a>\n"
            "📩 HR contact: @maryna_bon\n\n"
            "<b>📄 Contract Lawyer</b>\n"
            "🔹 3+ years legal experience\n"
            "🔹 Fluent English (B2–C1)\n"
            "🔹 Knowledge of payment systems or willingness to learn\n\n"
            "💰 Remote, flexible hours, paid vacation\n\n"
            "<b>🎯 Marketing Manager</b>\n"
            "🔹 4+ years in fintech/SaaS/startups\n"
            "🔹 SEO, SEM, content & automation skills\n"
            "🔹 Ambition to grow into CMO role\n\n"
            "💰 Competitive salary + bonuses\n\n"
            "<b>🧩 Customer Support Operator</b>\n"
            "🔹 1+ year in support\n"
            "🔹 Calm under pressure\n"
            "🔹 English B1+, tech-friendly\n\n"
            "📅 Shift schedule + Warsaw office optional"
        ),
        "social_media": (
            "<b>🌐 Join our social media</b>\n\n"
            "💬 <a href='https://t.me/todapaynews'>Telegram</a>\n"
            "📸 <a href='https://www.instagram.com/toda_pay'>Instagram</a>\n"
            "📘 <a href='https://www.facebook.com/todapay/'>Facebook</a>\n"
            "🐦 <a href='https://x.com/TODA_PAY'>X / Twitter</a>\n"
            "✍️ <a href='https://medium.com/@TODA_PAY'>Medium</a>\n"
            "🎵 <a href='https://www.tiktok.com/@todapay'>TikTok</a>\n"
            "💼 <a href='https://www.linkedin.com/company/transfer-of-digital-assets/'>LinkedIn</a>\n"
            "📝 <a href='https://todapay.com/blog'>Blog</a>"
        ),
        "hotline": (
            "<b>📞 Hot-line</b>\n\n"
            "💼 Sales contact: @BDTodaArt\n\n"
            "🧩 We offer a list of solutions with no setup fees.\n"
            "(Please contact us directly for more details.)"
        )
    }

    for section, text in defaults.items():
        c.execute("INSERT OR IGNORE INTO content (section, text) VALUES (?, ?)", (section, text))
    conn.commit()
    conn.close()


def get_content(section):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT text FROM content WHERE section = ?", (section,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "No content yet."


def update_content(section, new_text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE content SET text = ? WHERE section = ?", (new_text, section))
    conn.commit()
    conn.close()


def reset_content():
    defaults = {
        "who_we_are": (
            "<b>Who we are?</b>\n\n"
            "Founded in 2022, TODAPAY is built on a foundation of expertise in payment solutions, "
            "risk management, and financial operations. Our team has successfully developed fintech "
            "projects, facilitated international payments, and implemented alternative payment methods, "
            "ensuring businesses have access to secure, efficient, and scalable financial solutions.\n\n"
            "🌐 <a href='https://todapay.com/about-us'>More about us</a>"
        ),
        "join_team": (
            "<b>👥 Join our team</b>\n\n"
            "🌐 Career page: <a href='https://todapay.com/career'>todapay.com/career</a>\n"
            "📩 HR contact: @maryna_bon\n\n"
            "<b>📄 Contract Lawyer</b>\n"
            "🔹 3+ years legal experience\n"
            "🔹 Fluent English (B2–C1)\n"
            "🔹 Knowledge of payment systems or willingness to learn\n\n"
            "💰 Remote, flexible hours, paid vacation\n\n"
            "<b>🎯 Marketing Manager</b>\n"
            "🔹 4+ years in fintech/SaaS/startups\n"
            "🔹 SEO, SEM, content & automation skills\n"
            "🔹 Ambition to grow into CMO role\n\n"
            "💰 Competitive salary + bonuses\n\n"
            "<b>🧩 Customer Support Operator</b>\n"
            "🔹 1+ year in support\n"
            "🔹 Calm under pressure\n"
            "🔹 English B1+, tech-friendly\n\n"
            "📅 Shift schedule + Warsaw office optional"
        ),
        "social_media": (
            "<b>🌐 Join our social media</b>\n\n"
            "💬 <a href='https://t.me/todapaynews'>Telegram</a>\n"
            "📸 <a href='https://www.instagram.com/toda_pay'>Instagram</a>\n"
            "📘 <a href='https://www.facebook.com/todapay/'>Facebook</a>\n"
            "🐦 <a href='https://x.com/TODA_PAY'>X / Twitter</a>\n"
            "✍️ <a href='https://medium.com/@TODA_PAY'>Medium</a>\n"
            "🎵 <a href='https://www.tiktok.com/@todapay'>TikTok</a>\n"
            "💼 <a href='https://www.linkedin.com/company/transfer-of-digital-assets/'>LinkedIn</a>\n"
            "📝 <a href='https://todapay.com/blog'>Blog</a>"
        ),
        "hotline": (
            '💳 Choose your region to see available payment methods:'
        )
    }

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for section, text in defaults.items():
        c.execute("UPDATE content SET text = ? WHERE section = ?", (text, section))
    conn.commit()
    conn.close()
