import {Controller} from "stimulus";


export default class extends Controller {

    static targets = [
        "overlay",
    ]

    static classes = [
        "visible",
    ]

    connect() {
    }

    onToggle(e) {
        if (this.element.classList.contains(this.visibleClass)) {
            this.hide();
        } else {
            this.show();
        }
    }

    onClose(e) {
        this.hide();
    }

    show() {
        this.element.classList.add(this.visibleClass);
    }

    hide() {
        this.element.classList.remove(this.visibleClass);
    }

}
