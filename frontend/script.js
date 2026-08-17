const API_URL = "";

const pdfFiles = document.getElementById("pdfFiles");
const fileList = document.getElementById("fileList");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");

const question = document.getElementById("question");
const askBtn = document.getElementById("askBtn");

const answer = document.getElementById("answer");
const sources = document.getElementById("sources");


// Store selected files
let selectedFiles = [];


// ------------------------------
// PDF SELECTION
// ------------------------------

pdfFiles.addEventListener("change", () => {

    const newFiles = Array.from(pdfFiles.files);

    for (const file of newFiles) {

        if (file.type !== "application/pdf") {
            continue;
        }

        const alreadyExists = selectedFiles.some(
            existingFile =>
                existingFile.name === file.name &&
                existingFile.size === file.size
        );

        if (!alreadyExists) {
            selectedFiles.push(file);
        }
    }

    displayFiles();

    pdfFiles.value = "";
});


// ------------------------------
// DISPLAY SELECTED FILES
// ------------------------------

function displayFiles() {

    fileList.innerHTML = "";

    if (selectedFiles.length === 0) {
        fileList.innerHTML = "<p>No PDF files selected.</p>";
        return;
    }

    selectedFiles.forEach((file, index) => {

        const item = document.createElement("div");

        item.className = "file-item";

        item.innerHTML = `
            📄 ${file.name}

            <button
                type="button"
                onclick="removeFile(${index})"
            >
                Remove
            </button>
        `;

        fileList.appendChild(item);
    });
}


// ------------------------------
// REMOVE FILE
// ------------------------------

function removeFile(index) {

    selectedFiles.splice(index, 1);

    displayFiles();
}


// ------------------------------
// UPLOAD PDFs
// ------------------------------

uploadBtn.addEventListener("click", async () => {

    console.log("Upload button clicked");

    if (selectedFiles.length === 0) {

        uploadStatus.textContent =
            "Please select at least one PDF.";

        return;
    }

    const formData = new FormData();

    selectedFiles.forEach(file => {
        formData.append("files", file);
    });

    console.log("Files being uploaded:", selectedFiles);

    uploadStatus.textContent =
        "Uploading and processing documents...";

    uploadBtn.disabled = true;

    try {

        const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        console.log(
            "Upload response:",
            response.status
        );

        const data = await response.json();

        console.log(
            "Upload data:",
            data
        );

        if (!response.ok) {

            throw new Error(
                data.detail || "Upload failed"
            );
        }

        uploadStatus.textContent =
            `${data.files.length} PDF(s) uploaded successfully. ` +
            `${data.total_chunks} chunks created.`;

    } catch (error) {

        console.error(
            "UPLOAD ERROR:",
            error
        );

        uploadStatus.textContent =
            `Upload error: ${error.message}`;

    } finally {

        uploadBtn.disabled = false;
    }
});


// ------------------------------
// ASK QUESTION
// ------------------------------

askBtn.addEventListener("click", async () => {

    const userQuestion = question.value.trim();

    if (!userQuestion) {

        answer.textContent =
            "Please enter a question.";

        return;
    }

    answer.textContent = "Thinking...";

    sources.innerHTML = "";

    askBtn.disabled = true;

    try {

        const response = await fetch(
            `${API_URL}/ask?question=${encodeURIComponent(userQuestion)}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Request failed"
            );
        }

        answer.textContent = data.answer;


        // Display sources
        if (
            data.sources &&
            data.sources.length > 0
        ) {

            data.sources.forEach(source => {

                const item =
                    document.createElement("div");

                item.className =
                    "source-item";

                item.textContent =
                    `📄 ${source.filename} — Page ${source.page}`;

                sources.appendChild(item);
            });

        } else {

            sources.textContent =
                "No sources available.";
        }

    } catch (error) {

        answer.textContent =
            `Error: ${error.message}`;

        console.error(error);

    } finally {

        askBtn.disabled = false;
    }
});