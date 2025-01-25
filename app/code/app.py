from flask import Flask, render_template, request, jsonify
import pickle
import torch
import torchtext.data.utils as torchtext_data_utils
from utils import LSTMLanguageModel, generate, mock_star_wars_language_model

app = Flask(__name__)

# Load the pre-trained language model
lstm_data = pickle.load(open('models/lstm.pkl', 'rb'))
vocab = lstm_data['vocab']
vocab_size = lstm_data['vocab_size']
emb_dim = lstm_data['emb_dim']
hid_dim = lstm_data['hid_dim']
num_layers = lstm_data['num_layers']
dropout_rate = lstm_data['dropout_rate']
lstm = LSTMLanguageModel(vocab_size, emb_dim, hid_dim, num_layers, dropout_rate)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
lstm.load_state_dict(torch.load('models/best-val-lstm_lm.pt', map_location=device))
lstm.eval()
tokenizer = torchtext_data_utils.get_tokenizer('basic_english')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.get_json()
    user_prompt = data.get("prompt")
    if not user_prompt:
        return jsonify({"error": "Please provide a prompt."}), 400
    
    max_seq_len = 30
    seed = 0
    temperature = 0.8

    # Generate text
    generated_text = generate(user_prompt, max_seq_len, temperature, lstm, tokenizer, vocab, device, seed)
    generated_text = ' '.join(generated_text)
    return jsonify({"generated_text": generated_text})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
