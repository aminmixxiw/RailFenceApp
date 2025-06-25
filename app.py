from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def rail_fence_encrypt(text, rails):
    if rails <= 1 or rails >= len(text):
        return text, []

    fence = ['' for _ in range(rails)]
    rail_grid = [['' for _ in range(len(text))] for _ in range(rails)]
    rail = 0
    direction = 1

    for idx, char in enumerate(text):
        fence[rail] += char
        rail_grid[rail][idx] = char
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    return ''.join(fence), rail_grid

def rail_fence_decrypt(ciphertext, rails):
    if rails <= 1 or rails >= len(ciphertext):
        return ciphertext

    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    indexes = pattern * ((len(ciphertext) // len(pattern)) + 1)
    indexes = indexes[:len(ciphertext)]

    rail_counts = [indexes.count(i) for i in range(rails)]
    zigzag = [[] for _ in range(rails)]

    i = 0
    for r in range(rails):
        for _ in range(rail_counts[r]):
            zigzag[r].append(ciphertext[i])
            i += 1

    rail_indices = [0] * rails
    result = []
    for r in indexes:
        result.append(zigzag[r][rail_indices[r]])
        rail_indices[r] += 1

    return ''.join(result)

@app.route('/set_language', methods=['POST'])
def set_language():
    session['lang'] = request.form.get('lang', 'en')
    return redirect(url_for('index'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['history'] = []
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_text = ''
    rail_grid = []
    history = session.get('history', [])
    mode = request.form.get('mode', 'encrypt')
    lang = session.get('lang', 'en')

    if request.method == 'POST' and 'plaintext' in request.form:
        text = request.form.get('plaintext', '')
        rails = int(request.form.get('rails', 3))

        if mode == 'encrypt':
            encrypted_text, rail_grid = rail_fence_encrypt(text, rails)
        else:
            encrypted_text = rail_fence_decrypt(text, rails)

        history.insert(0, {'mode': mode, 'text': text, 'rails': rails, 'result': encrypted_text})
        session['history'] = history[:8]

    return render_template('index.html',
                           encrypted_text=encrypted_text,
                           rail_grid=rail_grid,
                           history=session.get('history', []),
                           mode=mode,
                           lang=lang)

if __name__ == '__main__':
    app.run(debug=True)