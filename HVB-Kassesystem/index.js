'use strict';
const escpos = require('escpos');
const path = require('path');

const device = new escpos.USB();
const printer = new escpos.Printer(device);

var express = require('express');

var app = express();

const http = require('http')

const server = http.createServer(function (request, response) {
    console.dir(request.param)

    if (request.method == 'POST') {
        console.log('POST')
        var body = ''
        request.on('data', function (data) {
            body += data
            console.log('Partial body: ' + body)
        })
        request.on('end', function () {
            console.log('Body: ' + body)
            response.writeHead(200, { 'Content-Type': 'text/html' })
            response.end('post received')

            print(JSON.parse(body))
        })
    } else {
        console.log('GET')
        var html = `ups`
        response.writeHead(200, { 'Content-Type': 'text/html' })
        response.end(html)
    }
})

const port = 9100
const host = '127.0.0.1'
server.listen(port, host)
console.log(`Listening at http://${host}:${port}`)

function print(printData) {
    printData = printData.sort(function IHaveAName(a, b) { // non-anonymous as you ordered...
        return b["Vare"] < a["Vare"] ? 1 // if b should come earlier, push a to end
            : b["Vare"] > a["Vare"] ? -1 // if b should come later, push a to begin
                : 0;                   // a and b are equal
    });

    console.log(printData);

    const logo = path.join(__dirname, 'hvb_logo_margin_negativ_scaled.png');
    escpos.Image.load(logo, function (image) {

        device.open(function () {
            printer.align('ct')
            printer.raster(image)
            printer
                .font('a')
                .encode('cp850')
                .size(2, 2)
                .control('lf')
                .text('Hedelands Veteranbane')
                .size(1, 1)
                .text(' - Nyd naturen langsomt')
                .control('lf')
                .control('lf')
                .align('rt');
            var cols = 48 - 4;
            for (var i = 0; i < printData.length; i++) {
                var priceString = parseFloat(printData[i]["Samlet pris"]).toFixed(2)
                var productsString = printData[i]["Antal"] + " " + printData[i]["Vare"]
                var columnsInBetween = cols - priceString.length - productsString.length
                printer.text(productsString + " ".repeat(columnsInBetween) + priceString)
            }
            printer.control('lf');
            var total = 0;
            var herafMoms = 0;
            for (var i = 0; i < printData.length; i++) {
                total += parseFloat(printData[i]["Samlet pris"]);
                herafMoms += (parseFloat(printData[i]["Moms"]) / 100) * parseFloat(printData[i]["Samlet pris"]);
            }
            var priceString = herafMoms.toFixed(2);
            var productsString = "Heraf moms";
            var columnsInBetween = cols - priceString.length - productsString.length;
            printer.text(productsString + " ".repeat(columnsInBetween) + priceString);
            
            var priceString = total.toFixed(2);
            var productsString = "Total";
            var columnsInBetween = cols - priceString.length - productsString.length;
            printer.text(productsString + " ".repeat(columnsInBetween) + priceString);
            printer
                .control('lf')
                .align('lt')
                .text("    Købsdato: " + (new Date().toLocaleString()))
                .text("    CVR: 56570756")
                .control('lf')
                .control('lf')
                .size(1, 1)
                .align('ct')
                .text("Vidste du, at vi også har løvfalds- og\n juletræstog? Se mere på ibk.dk!")
                .control('lf')
                .font('b')
                .align('ct')
                .text("\nHedelands Veteranbane - Brandhøjgårdsvej 2, 2640 Hedehusne")
            printer.cashdraw()
            //printer.cashdraw(2)
            //printer.cashdraw(5)
            printer.cut().close();
        });
    });
}