import {Controller} from "stimulus";


export default class extends Controller {

    // static values = {
    //     "inputVisible": Boolean,
    // }

    static targets = [
        "form",
            "email",
            "name",
            "submit",
            "message",
    ]

    // static classes = [
    //     "visible",
    // ]

    connect() {
    }

    handleSubmit(e) {
        e.preventDefault();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        // https://www.youtube.com/watch?v=4qek1pbjNeY / webpack / babel / fetch / IE11!
        fetch(this.formTarget.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                // 'Content-Type': 'application/json',
            },
            body: new FormData(this.formTarget)
        })
            .then(res => res.json())
            .then(this.handleResult.bind(this))
            .catch(error => {
                // enter your logic for when there is an error (ex. error toast)
                console.log(error)
            })
        this.emailTarget.disabled = true;
        this.nameTarget.disabled = true;
        this.submitTarget.disabled = true;
    }

    handleResult(data) {
        this.messageTarget.innerHTML = data.message;
        this.emailTarget.disabled = false;
        this.nameTarget.disabled = false;
        this.submitTarget.disabled = false;
        if (data.ok) {
            this.emailTarget.remove();
            this.nameTarget.remove();
            this.submitTarget.remove();
        } else {
            this.emailTarget.classList.remove('error');
            this.nameTarget.classList.remove('error');
            for (const error of data.errors) {
                this[error + "Target"].classList.add('error')
            }
        }
    }

}
