function generateTimetable() {
    let days = document.getElementById("days").value;
    let periods = document.getElementById("periods").value;

    if (days == "" || periods == "") {
        alert("Please fill all fields");
        return;
    }

    let output = "<table><tr><th>Day / Period</th>";

    for (let p = 1; p <= periods; p++) {
        output += "<th>P" + p + "</th>";
    }
    output += "</tr>";

    for (let d = 1; d <= days; d++) {
        output += "<tr><th>Day " + d + "</th>";
        for (let p = 1; p <= periods; p++) {
            output += "<td>Subject</td>";
        }
        output += "</tr>";
    }

    output += "</table>";

    document.getElementById("output").innerHTML = output;
}