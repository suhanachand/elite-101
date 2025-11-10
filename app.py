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
        "<button onclick=\"sendMessage('4')\">4. Exit</button>"
    )


def handle_menu_selection(choice):
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

    elif choice in ["4", "exit"]:
        name = user_data["name"].capitalize()
        user_data.update({"name": "", "age": "", "step": 0, "total": 0.0, "order": []})
        return f"👋 Thank you, {name}! Have a flavorful day! 🍛"

    else:
        return "I didn’t understand that. Please choose a number (1–6)."






if __name__ == "__main__":
    app.run(debug=True)
