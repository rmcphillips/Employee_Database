const mprnContainer = document.getElementById("div_id_mprn");
const gprnContainer = document.getElementById("div_id_gprn");
const saleType = document.getElementById("id_sale_type");
const btnSubmit = document.getElementById("btnSubmit");
const mprnInput = mprnContainer.children[1].children[0]
const gprnInput = gprnContainer.children[1].children[0]

// Loads hidden by default
mprnContainer.hidden = true
gprnContainer.hidden = true


saleType.addEventListener("change", () => {
    let saleTypeValue = saleType.options[saleType.selectedIndex].value;
    showInputs(saleTypeValue)
    btnSubmit.disabled = true
})

const showInputs = (saleTypeValue) => {
    switch (saleTypeValue) {
        case "ELE":
            clearInputs()
            mprnContainer.hidden = false
            gprnContainer.hidden = true
            break;
        case "NGAS":
            clearInputs()
            mprnContainer.hidden = true
            gprnContainer.hidden = false
            break;
        case "NDUAL":
            clearInputs()
            mprnContainer.hidden = false
            gprnContainer.hidden = false
            break;
        default:
            break;
    }
}

const clearInputs = () => {
    mprnInput.value = ""
    gprnInput.value = ""
}


// Disable submit button in case MPRN in wrong format
mprnInput.addEventListener("keyup", () => {

    if ((mprnInput.value.length != 11 || gprnInput.value.length != 7) && saleType.value === "NDUAL") {
        btnSubmit.disabled = true
    }
    else {
        btnSubmit.disabled = false
    }
})

// Disable submit button in case GPRN in wrong format
gprnInput.addEventListener("keyup", () => {

    if ((mprnInput.value.length != 11 || gprnInput.value.length != 7) && saleType.value === "NDUAL") {
        btnSubmit.disabled = true
    }
    else {
        btnSubmit.disabled = false
    }
})

