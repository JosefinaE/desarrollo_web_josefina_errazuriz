// Validates email using regex
// Code extracted from https://stackoverflow.com/a/46181
const validateEmail = (email) => {
  const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  const input =  String(email).toLowerCase()
  return emailRegex.test(input)
};

function validateName(name, minlength){
    return name.trim().length >= 3
}

// accepts phone numbers in the format
// +xxxxxxxxx (whitespaces allowed)
function validatePhone(phoneNumber){
    const phoneRegex = /^\+[0-9]{7,15}$/ // matches'+' and 7 to 15 digits between 0-9
    const whitespaceRegex = / /g
    const input = String(phoneNumber).replace(whitespaceRegex,'')
    return phoneRegex.test(input)
}

// validates a week of hours
function validateHoursArray(horas) {
    for (let i = 0; i < horas.length; i++) {
            const val = horas[i].trim();
            if (val !== "") {
                const num = Number(val);
                if (isNaN(num) || num < 0 || num > 24) {
                    return false;
                }
            }
        }
    return true;
}

function validateFiles(files) {
    if (!files || files.length === 0) return false;
    for (let i = 0; i < files.length; i++) {
        const type = file[i].type;
        if (!type.startsWith("image/") && !type.startsWith("video/")) {
            return false;
        }
    }
    return true;
}

function validateURL(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}