from flask import Flask, render_template, request, session, redirect, url_for
#Flask is to create the web application
#render_template is to show HTML pages using templates
#request is to get data sent by the user (like form input)
#session is to store user data (like language or history)
#redirect is to send the user to another page
#url_for is to get the URL of a route (like 'index')

#Create the Flask app and set a secret key for sessions
app = Flask(__name__)
app.secret_key = 'supersecretkey'

#Return original text if rails are too few or more than text length
def rail_fence_encrypt(text, rails):
    if rails <= 1 or rails >= len(text):
        return text, []


    fence = ['' for _ in range(rails)] #List to store characters for each rail
    rail_grid = [['' for _ in range(len(text))] for _ in range(rails)] #2D grid to visualize zigzag pattern
    rail = 0
    direction = 1 #Initial direction (1 = down, -1 = up)

#Loop through text to place each character in zigzag rail pattern
    for idx, char in enumerate(text): #Go through each letter in the text with its position number
        fence[rail] += char # Add the letter to the current rail
        rail_grid[rail][idx] = char # Put the letter in the rail grid at the correct row and column
        rail += direction #Move to the next rail (up or down)
        if rail == 0 or rail == rails - 1: #If at the top or bottom rail, it will change direction
            direction *= -1

#Combine all rails into the final encrypted text and return it with the rail grid
    return ''.join(fence), rail_grid

#Return original text if rail count is invalid
def rail_fence_decrypt(ciphertext, rails):
    if rails <= 1 or rails >= len(ciphertext):
        return ciphertext

#Generate the zigzag pattern of rail indexes to determine the order of character placement
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1)) #Dptkan pattern dia semula
    indexes = pattern * ((len(ciphertext) // len(pattern)) + 1) #Make the zigzag pattern long enough to match the number of letters in the ciphertext.
    indexes = indexes[:len(ciphertext)]

#Count how many characters go into each rail and prepare empty lists to hold them
    rail_counts = [indexes.count(i) for i in range(rails)]
    zigzag = [[] for _ in range(rails)]

#Fill each rail with the appropriate number of characters from the ciphertext
    i = 0
    for r in range(rails):
        for _ in range(rail_counts[r]):
            zigzag[r].append(ciphertext[i])
            i += 1

#Build back the original text by taking letters from each rail in zigzag order - for decrypt
    rail_indices = [0] * rails
    result = []
    for r in indexes:
        result.append(zigzag[r][rail_indices[r]])
        rail_indices[r] += 1

    return ''.join(result)

#Set the selected language
@app.route('/set_language', methods=['POST'])
def set_language():
    session['lang'] = request.form.get('lang', 'en')
    return redirect(url_for('index'))

#Clear the encryption or descryption history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['history'] = []
    return redirect(url_for('index'))

#Set defaults for output, grid, history, mode, and language
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
        session['history'] = history[:5]

    return render_template('index.html',
                           encrypted_text=encrypted_text,
                           rail_grid=rail_grid,
                           history=session.get('history', []),
                           mode=mode,
                           lang=lang)

#To start the app
if __name__ == '__main__':
    app.run(debug=True)