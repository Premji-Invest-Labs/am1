# AM1
`Ajna MultiAgent One` platform to get things done for you from surfing web and taking actions, collecting data, reading and analysing files, planning, coding, research, and
more... to reach the goal given by user.

Let agents do the grunt work for you, while you focus on the big picture.

## Demo Video
Demo video will be released on 11th March 2025 along with UI Release.

## Setup
Execute the following commands to setup the project:
```bash setup.sh```

## Run AM1
Execute the following commands to run the project:
```bash run_dockerized.sh```

## Documentation
Key things to note:
- You can run LLM models locally only if your system has GPU, sufficient RAM, compute and space. Please check the requirements before running the models.
- If you do not have sufficient resources in your local system, you can use LLMs on cloud of your choice. For instance, you will need to specify OpenAI Key in config/local.yml file or as environment variable in your system or dockerfile as applicable. 
- More LLM support will be added soon.
- We have currently integrated MagenticOne (Autogen 0.4.2) for our Multi-Agent Framework. Refer to the documentation of MagenticOne for more details.
- More such frameworks will be added soon so that users can choose which works best for them.
- For privacy, we recommend using any open-source LLM model on your local system with an open source model where data never leaves your system.
- For any queries, you can raise an issue in GitHub repo.
- We will share Contributors guide on 11th March 2025.
- Please note this is an active development product, and we are working on adding more features and support for more frameworks. Things may change rapidly and sometimes break, please do not consider using this for production grade application or critical workflow.
- Feel free to share your feedback and suggestions.
- The project may change rapidly, please keep an eye on the updates and documentation for best use.

## License
This project is licensed under Apache 2.0 License - see the LICENSE file for details.

## References
- [AutoGen](https://github.com/microsoft/autogen)
- [AG2](https://github.com/ag2ai/ag2)
- [OpenAI](https://openai.com)


## Development Setup

### Setting Up and Running Pre-Commit Hooks

**Prerequisites**

- Python (version 3.x)

- Git installed on your system

**Installation**

1. Install pre-commit:

```bash
pip install pre-commit
```

Alternatively, for macOS:
```bash
    brew install pre-commit
```
2.Set up pre-commit in your repository:
```bash
    pre-commit install
```
3.Verify the installation:

```bash
pre-commit run --all-files
```

This runs all hooks on existing files.


Here’s a more structured and readable version of your document in Markdown format:

### Setting Up GPG Signing Keys for Git

#### 1. Install GPG

- **Linux (Debian/Ubuntu)**:
    ```bash
    sudo apt install gnupg
    ```

- **MacOS (Homebrew)**:
    ```bash
    brew install gnupg
    ```

- **Windows**:
    - Install Gpg4win from [https://www.gpg4win.org/](https://www.gpg4win.org/).

#### 2. Generate a GPG Key

1. Run the following command:
    ```bash
    gpg --full-generate-key
    ```

2. Choose the following options:
    - **Key type**: RSA and RSA (default)
    - **Key size**: 4096
    - **Validity**: Never expire (or set an expiration)
    - **Enter your name, email, and passphrase**

3. List your generated keys:
    ```bash
    gpg --list-secret-keys --keyid-format=long
    ```

   Example output:
    ```bash
    sec rsa4096/ABCDEF1234567890 2024-03-07 [SC]
    Key fingerprint = ABCD 1234 EFGH 5678 IJKL 9012 MNOP QRST UVWX YZ12
    ```

4. Copy the key ID (e.g., `ABCDEF1234567890`).

---

#### 3. Configure Git to Use GPG

1. **Export the GPG key**:
    ```bash
    gpg --armor --export ABCDEF1234567890
    ```

2. **Add the key to Git**:
    ```bash
    git config --global user.signingkey ABCDEF1234567890
    ```

3. **Enable commit signing**:
    ```bash
    git config --global commit.gpgSign true
    ```

---

#### 4. Verify GPG Signing

1. Make a signed commit:
    ```bash
    git commit -S -m "Signed commit"
    ```

2. Check if the commit is signed:
    ```bash
    git log --show-signature -1
    ```

---

### Adding Your GPG Key to GitHub/GitLab

#### 1. Export Your GPG Public Key

Run the following command to get your public key:
```bash
gpg --armor --export YOUR_KEY_ID
```
Example output:

```bash
-----BEGIN PGP PUBLIC KEY BLOCK-----
...
-----END PGP PUBLIC KEY BLOCK-----
```
Copy everything from -----BEGIN PGP PUBLIC KEY BLOCK----- to -----END PGP PUBLIC KEY BLOCK-----.


#### 2. Add the Key to GitHub

1.	Go to GitHub → Settings → SSH and GPG keys.
2.	Click New GPG key.
3.	Paste your public key and click Add GPG key.
4.	Verify by making a signed commit and pushing it:
```bash
  git commit -S -m "Signed commit"
  git push
```

#### 3. Add the Key to GitLab

1.	Go to GitLab → Preferences → GPG Keys.
2.	Click Add GPG key.
3.	Paste your public key and save.
4.	Verify by making a signed commit and pushing it:
	
```bash
git commit -S -m "Signed commit"
git push
```

  Now your commits will show as “Verified” on GitHub/GitLab!

---

