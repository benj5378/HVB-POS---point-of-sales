var Service = require('node-windows').Service;

// Create a new service object
var svcPrinterService = new Service({
  name:'HVB-Kassesystem - Printer',
  description: 'Printer service for HVB-Kassesystem',
  script: require('path').join(__dirname,'index.js'),
  nodeOptions: [
    '--harmony',
    '--max_old_space_size=4096'
  ]
});

// Listen for the "install" event, which indicates the
// process is available as a service.
svcPrinterService.on('install',function(){
  svcPrinterService.start();
});

svcPrinterService.uninstall();

var svcPrinterService = require('node-windows').Service;

//####################################################

// Create a new service object
var svcStatistics = new Service({
  name:'HVB-Kassesystem - Statistikserver',
  description: 'Statistikserver for HVB-Kassesystem',
  script: require('path').join(__dirname,'statistics/bin/www.js'),
  nodeOptions: [
    '--harmony',
    '--max_old_space_size=4096'
  ]
});

// Listen for the "install" event, which indicates the
// process is available as a service.
svcStatistics.on('install',function(){
  svcStatistics.start();
});

svcStatistics.uninstall();