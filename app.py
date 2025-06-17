from flask import Flask, render_template, request

app = Flask(__name__)

def rail_fence_encrypt(text, rails):
    if rails <= 1 or rails >= len(text):
        return text, []

    # Create the fence as a list of empty strings for each rail
    fence = ['' for _ in range(rails)]
    rail_grid = [['' for _ in range(len(text))] for _ in range(rails)]

    rail = 0
    direction = 1  # 1 for down, -1 for up

    for idx, char in enumerate(text):
        fence[rail] += char
        rail_grid[rail][idx] = char

        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    encrypted = ''.join(fence)
    return encrypted, rail_grid

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_text = ''
    rail_grid = []

    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        rails = int(request.form.get('rails', 3))

        encrypted_text, rail_grid = rail_fence_encrypt(plaintext, rails)

    return render_template('index.html',
                           encrypted_text=encrypted_text,
                           rail_grid=rail_grid)

if __name__ == '__main__':
    app.run(debug=True)
