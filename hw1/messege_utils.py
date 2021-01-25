def preprocess_message(message, alphabet):
    message = message.lower()
    message = ''.join(char for char in message if char in alphabet)
    return message