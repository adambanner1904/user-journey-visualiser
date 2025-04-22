const addProject = document.querySelector("#add-project-button");
const dialog = document.querySelector("#data-upload")
const closeButton = document.querySelector("#close-button")

addProject.addEventListener("click", (event) => {
  dialog.showModal()
});

closeButton.addEventListener("click", event => {
    dialog.close()
})