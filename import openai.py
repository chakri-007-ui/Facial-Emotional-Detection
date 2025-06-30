import openai.py
from flask import Flask, request, jsonify

# Set up the OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

app = Flask(__name__)

# A route for generating an image from a text prompt
@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        # Extract the prompt from the request
        prompt = request.json.get('prompt', None)
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Generate the image using OpenAI's image API
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size='1024x1024'
        )

        # Get the generated image URL
        image_url = response['data'][0]['url']
        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# A route for handling chatbot text input
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Extract the user message from the request
        user_message = request.json.get('message', None)
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Here you can add logic for detecting if the message is related to image generation
        if 'generate an image of' in user_message.lower():
            # Extract the part of the message that specifies the image prompt
            prompt = user_message.lower().replace('generate an image of', '').strip()
            return generate_image_helper(prompt)

        # For regular chatbot responses, use GPT to respond
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f'User: {user_message}\nAI:',
            max_tokens=150,
            temperature=0.7
        )

        # Extract the chatbot's response
        bot_response = response['choices'][0]['text'].strip()
        return jsonify({'response': bot_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_image_helper(prompt):
    try:
        # Call the generate_image function internally
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size='1024x1024'
        )
        image_url = response['data'][0]['url']
        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
