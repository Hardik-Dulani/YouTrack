import pickle
from pathlib import Path
import streamlit_authenticator as stauth
names = ["Hardik Dulani", "Ipshita De"]
usernames = ["hardik.dulani", "ipss1902"]
passwords = ["hahahaha", "hehehehe"]
hashed_passwords = stauth.Hasher (passwords).generate()