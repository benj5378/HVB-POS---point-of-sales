function start() {
    render();
}

function render() {
    console.log(data);
    var total = {};
    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data[i]["receipt"].length; j++) {
            console.log(data[i]["receipt"][j]);
            if (!(data[i]["paymentMethod"] in total)) {
                total[data[i]["paymentMethod"]] = 0;
            }
            total[data[i]["paymentMethod"]] += parseFloat(data[i]["receipt"][j]["Samlet pris"]);
        }
    }
    console.log(total);
    var TOTAL = 0
    paymentMethods = Object.keys(total)
    var insert = document.getElementById("keyFigures")
    for (var i = 0; i < paymentMethods.length; i++) {
        insert.childNodes[0].innerHTML += "<p>" + paymentMethods[i] + ": " + total[paymentMethods[i]] + " kroner</p>";
        TOTAL += total[paymentMethods[i]]
    }
    insert.childNodes[0].innerHTML += "<p>Totalt: " + TOTAL + " kroner</p>"


    var myPieChart = new Chart(insert.childNodes[1].childNodes[0], {
        type: 'pie',
        data: {
            labels: paymentMethods,
            datasets: [{
                label: '# of Votes',
                data: Object.values(total),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {}
    });


    insert = document.getElementById("products");
    var varer = get();
    html = "<table><thead><tr><th>Vare</th><th>Samlet beløb</th></tr></thead><tbody>";
    for (var i = 0; i < Object.keys(varer).length; i++) {
        html += "<tr><td>" + Object.keys(varer)[i] + "</td><td>" + Object.values(varer)[i] + " kroner</td></tr>";
    }
    html += "</tbody></table>";
    insert.childNodes[0].innerHTML += html;

    var myPieChart2 = new Chart(insert.childNodes[1].childNodes[0], {
        type: 'pie',
        data: {
            labels: Object.keys(varer),
            datasets: [{
                label: '# of Votes',
                data: Object.values(varer),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {}
    });
}

function get() {
    console.log("\n\\/\\/\\/\\/\\/\\/\\/\\/\n")
    var varer = {};
    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data[i]["receipt"].length; j++) {
            console.log(data[i]["receipt"][j]["Vare"]);
            console.log(parseFloat(data[i]["receipt"][j]["Samlet pris"]));
            if (!(data[i]["receipt"][j]["Vare"] in varer)) {
                varer[data[i]["receipt"][j]["Vare"]] = 0;
            }
            varer[data[i]["receipt"][j]["Vare"]] += parseFloat(data[i]["receipt"][j]["Samlet pris"]);
        }
    }
    console.log(varer);
    return varer;
}