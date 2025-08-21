# 代码生成时间: 2025-08-21 18:49:48
import hashlib
def calculate_hash(data, algorithm='sha256', encoding='utf-8', errors='strict', hex=False):
    """
    Calculate the hash of the provided data using the specified algorithm.

    Args:
        data (str): The data to be hashed.
        algorithm (str): Hashing algorithm to use (default: 'sha256').
        encoding (str): Encoding of the input data (default: 'utf-8').
        errors (str): Error handling scheme for encoding errors (default: 'strict').
        hex (bool): Return the hash as a hexadecimal string (default: False).

    Returns:
        hash_value: The hash value of the input data.
    """
    if not isinstance(data, str):
        raise TypeError("Input data must be a string.")

    try:
        digest = getattr(hashlib, f"{algorithm}")()
        digest.update(data.encode(encoding, errors))

        if hex:
            return digest.hexdigest()
        else:
            return digest.digest()
    except AttributeError:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    except (TypeError, UnicodeEncodeError) as e:
        raise ValueError(f"Failed to encode data: {e}")

def main():
    # Example usage of the hash calculator
    data = "Hello, world!"
    algorithm = "sha256"
    hash_value = calculate_hash(data, algorithm)
    print(f"{algorithm} hash of '{data}': {hash_value}")
def make_app():
    """
    Create a Tornado application.
    """
    from tornado.web import RequestHandler, Application
    class HashHandler(RequestHandler):
        def get(self):
            data = self.get_argument("data", "")
            algorithm = self.get_argument("algorithm", "sha256")
            hex = self.get_argument("hex", "False").lower() == "true"
            try:
                hash_value = calculate_hash(data, algorithm, hex=hex)
                if hex:
                    self.write(f"Hash: {hash_value}")
                else:
                    self.write(f"Hash: {hash_value}")
            except Exception as e:
                self.write(f"Error: {str(e)}")

    app = Application([(r"/hash", HashHandler)])
    return app
def run_server():
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
def if __name__ == "__main__":
    run_server()
