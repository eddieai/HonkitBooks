# How to build a book using Honkit

## Prerequisites: Install Node.js, npm and yarn

- Download and install `nvm`:
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  ```

- Download and install Node.js:
  ```bash
  nvm install 22
  ```

- Verify the Node.js version:
  ```bash
  node -v
  nvm current
  ```

- Verify npm version:
  ```bash
  npm -v
  ```

- Download and install Yarn:
  ```bash
  corepack enable yarn
  ```

- Verify Yarn version:
  ```bash
  yarn -v
  ```

## 1. Install HonKit locally inside book project

Navigate to **book project**:

a. install Honkit locally.

- Using NPM:
  ```bash
  npm init --yes
  npm install honkit --save-dev
  ```

b. create a .gitignore file:

```bash
echo -e "node_modules\n.git" > .gitignore
```


## 2. Create ./docs folder

a. create **./docs** folder:

```bash
mkdir docs
```

b. make sure all markdown files are inside this folder

c. make sure there is **README.md** and **SUMMARY.md**

- **README.md** is the first page of the book
- **SUMMARY.md** is the table of content with links to all sub pages


## 3. Build Honkit

### Build using bash script (Suggested)

Directly run bash script:
```bash
scripts/build_honkit_books.sh --BOOK BOOK_NAME --GIT --COMMIT_MSG MESSAGE
```

For example:
```bash
scripts/build_honkit_books.sh --BOOK interpy-zh --GIT --COMMIT_MSG test
```

Or build manually by running the following commands.

### Build maually

From **./docs** folder:

a. build book using:

```bash
npx honkit init
npx honkit build
```

b. move generated _book content to ./docs

```bash
rm -rf ./gitbook && mv ./_book/* ./ && rm -rf ./_book
```


## 4. Create Github page

a. push to Github

b. Go to Github book project page, select **Settings -> Pages**

c. In "Build and deployment", select "**Deploy from a branch**" -> "**master**" "**/docs**"
