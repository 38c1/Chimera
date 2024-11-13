# Download Chimera/examples/sprite3/chimeraclient.sprite3 for this to work!

# Make sure to set the variable names.

import requests
import time

# Load and execute chimera.py from URL
exec(requests.get("https://raw.githubusercontent.com/38c1/Chimera/refs/heads/main/chimera/chimera.py").text)

# Create array with first 10 spots empty, then alphabet
cipher = [None] * 10 + list('_abcdefghijklmnopqrstuvwxyz')

def encode(text):
    return ''.join(str(cipher.index(c)) for c in text.lower())

def decode(numbers):
    result = ''
    i = 0
    try:
        while i < len(numbers):
            num = int(numbers[i:i+2])
            result += cipher[num]
            i += 2
        return result
    except Exception as e:
        print(f"Error decoding: {e}")
        return None

# Main execution
def main():
    # Create an instance of Chimera
    cloud = Chimera(
        project_id="",
        session_id="",
        username=""
    )

    try:
        # Call connect() on cloud instance
        if not cloud.connect():
            raise Exception("Failed to establish initial connection")

        while True:
            try:
                # Call get_var() on cloud instance
                decoded = decode(cloud.get_var("Client1"))
                if decoded:
                    # Reverse the decoded string and set both variables
                    reversed_decoded = decoded[::-1]

                    # ABC followed by the reversed string
                    if not cloud.set_var("Server1", encode("abc_" + reversed_decoded)):
                        print("Failed to set first variable, retrying...")
                        continue

                    time.sleep(1)

                    # Set the reversed string followed by ABC
                    if not cloud.set_var("Server1", encode(reversed_decoded + "_abc")):
                        print("Failed to set second variable, retrying...")
                        continue

                    time.sleep(1)
                else:
                    print("Failed to decode, waiting before retry...")
                    time.sleep(5)
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)  # Wait before retrying

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        # Call close() on cloud instance
        cloud.close()

if __name__ == "__main__":
    main()
