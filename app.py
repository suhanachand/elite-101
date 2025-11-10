from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

user_data = {"name": "", "age": "", "step": 0, "total": 0.0, "order": []}

menu = {
    "paneer butter masala": 12.99,
    "chicken biryani": 13.99,
    "tandoori mix grill": 15.99,
    "garlic naan": 3.99,
    "mango lassi": 4.49,
    "gulab jamun": 5.99,
    "thumbs up": 1.99
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()
    step = user_data["step"]
    response = ""

    if step == 0:
        response = "Namaste! 🙏 Welcome to <b>NamasteBot</b> — your Indian Restaurant Assistant.<br>What’s your name?"
        user_data["step"] = 1

    elif step == 1:
        user_data["name"] = user_message
        response = f"Nice to meet you, {user_data['name'].capitalize()}! How old are you?"
        user_data["step"] = 2

    elif step == 2:
        user_data["age"] = user_message
        response = f"Perfect, {user_data['name'].capitalize()}! Here’s how I can help you today:<br><br>" + show_menu()
        user_data["step"] = 3

    elif step == 3:
        response = handle_menu_selection(user_message)

    elif step == 4:
        response = handle_order(user_message)

    return jsonify({"reply": response})


def show_menu():
    """Main menu."""
    return (
        "<b>Menu Options:</b><br>"
        "<button onclick=\"sendMessage('1')\">1️. View Menu</button><br>"
        "<button onclick=\"sendMessage('2')\">2️. Today's Specials</button><br>"
        "<button onclick=\"sendMessage('3')\">3. Restaurant Info</button><br>"
        "<button onclick=\"sendMessage('4')\">4. Make a Reservation</button>"
        "<button onclick=\"sendMessage('5')\">5. Exit</button>"
    )


def handle_menu_selection(choice, message=None):
    """Menu options."""
    if choice in ["1", "menu"]:
        menu_list = "<br>".join([f"{i.title()} - ${p:.2f}" for i, p in menu.items()])
        return f"🍲 <b>Our Menu:</b><br>{menu_list}<br><br>{show_menu()}"

    elif choice in ["2", "specials"]:
        return (
            "🌶️ <b>Today's Specials:</b><br>"
            "- Tandoori Mix Grill - $15.99<br>"
            "- Mango Lassi Combo - $10.99<br><br>"
            + show_menu()
        )

    elif choice in ["3", "info"]:
        return (
            "📍 <b>Namaste Indian Kitchen</b><br>"
            "Located at 45 Spice Street, Phoenix, AZ<br>"
            "Hours: 11 AM – 10 PM<br>"
            "Call at (602) 555-1212<br><br>"
            + show_menu()
        )

    elif choice in ["4", "reservation"]:
        # Initialize reservation process
        if "reservation_step" not in user_data or user_data.get("reservation_step") == 0:
            user_data["reservation_step"] = 1
            user_data["reservation"] = {}
            return "🪷 Let's make your reservation!<br>Please enter your full name:"

        # Step 1: Get name
        elif user_data["reservation_step"] == 1:
            user_data["reservation"]["name"] = message.strip().title()
            user_data["reservation_step"] = 2
            return "How many people will be dining?"

        # Step 2: Get number of people
        elif user_data["reservation_step"] == 2:
            if not message.isdigit() or int(message) <= 0:
                return "Please enter a valid number of guests."
            user_data["reservation"]["people"] = int(message)
            user_data["reservation_step"] = 3
            return "On which date would you like to reserve? (e.g., 2025-11-12)"

        # Step 3: Get date
        elif user_data["reservation_step"] == 3:
            user_data["reservation"]["date"] = message.strip()
            user_data["reservation_step"] = 4
            return "At what time? (e.g., 7:30 PM)"

        # Step 4: Get time
        elif user_data["reservation_step"] == 4:
            user_data["reservation"]["time"] = message.strip()
            user_data["reservation_step"] = 5
            return "Would you like to leave a special request or occasion note? (Type 'none' if not applicable)"

        # Step 5: Get special request
        elif user_data["reservation_step"] == 5:
            note = message.strip()
            if note.lower() != "none":
                user_data["reservation"]["note"] = note
            else:
                user_data["reservation"]["note"] = "None"

            # Reservation complete
            name = user_data["reservation"]["name"]
            people = user_data["reservation"]["people"]
            date = user_data["reservation"]["date"]
            time = user_data["reservation"]["time"]
            note = user_data["reservation"]["note"]

            # Reset steps
            user_data["reservation_step"] = 0

            return (
                f"✅ Your reservation has been successfully made, {name}!<br><br>"
                f"📅 Date: {date}<br>"
                f"⏰ Time: {time}<br>"
                f"👥 Guests: {people}<br>"
                f"📝 Special Request: {note}<br><br>"
                f"Thank you for choosing Namaste Indian Kitchen — we look forward to serving you! 🍛"
            )

    elif choice in ["5", "exit"]:
        name = user_data["name"].capitalize()
        user_data.update({"name": "", "age": "", "step": 0, "total": 0.0, "order": []})
        return f"👋 Thank you, {name}! Have a flavorful day! 🍛"

    else:
        return "I didn’t understand that. Please choose a number (1–6)."
