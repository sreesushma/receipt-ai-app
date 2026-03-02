const form = document.getElementById("uploadForm")
const resultBox = document.getElementById("result")
const loading = document.getElementById("loading")
const fileInput = document.getElementById("fileInput")
const previewImage = document.getElementById("previewImage")
const previewContainer = document.getElementById("previewContainer")

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0]
    if (!file) return

    previewImage.src = URL.createObjectURL(file)
    previewContainer.classList.remove("hidden")
})

form.addEventListener("submit", async (e) => {
    e.preventDefault()

    const file = fileInput.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    loading.classList.remove("hidden")
    resultBox.innerHTML = ""

    try {
        const res = await fetch("/analyze", {
            method: "POST",
            body: formData
        })

        const data = await res.json()

        resultBox.innerHTML = `
            <div class="bg-white/10 p-4 rounded-xl">
                <div><strong>Store:</strong> ${data.store || "N/A"}</div>
                <div><strong>Date:</strong> ${data.date || "N/A"}</div>
                <div><strong>Total:</strong> ${data.total || "N/A"}</div>
                <div class="mt-2">
                    <strong>Items:</strong>
                    <ul class="list-disc ml-5">
                        ${(data.items || []).map(i => `<li>${i}</li>`).join("")}
                    </ul>
                </div>
            </div>
        `
    } catch (err) {
        console.error(err)
        resultBox.innerHTML = "Error analyzing receipt"
    }

    loading.classList.add("hidden")
})