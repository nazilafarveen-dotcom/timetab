function login() {
    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    // Temporary login (replace with backend later)
    if (user === "admin" && pass === "admin123") {
        window.location.href = "D:\timetablesystem\templates\dashboard.html";
    } else {
        document.getElementById("error").innerText = "Invalid Login!";
    }
}