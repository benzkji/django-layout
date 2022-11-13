import {Controller} from "stimulus";


export default class extends Controller {

    static values = {
        "inputVisible": Boolean,
    }

    static targets = [
        "input",
    ]

    static classes = [
        "visible",
    ]

    connect() {
        if (this.inputTarget.value) {
            this.show();
        }
    }

    handleSubmit(e) {
        if (!this.inputTarget.value || !this.inputTarget.classList.contains(this.visibleClass)) {
            e.preventDefault();
            this.show();
            this.inputTarget.focus();
        }
    }

    onClose(e) {
        this.hide();
    }

    show() {
        this.inputTarget.classList.add(this.visibleClass);
    }

    hide() {
        this.inputTarget.classList.remove(this.visibleClass);
    }

}
