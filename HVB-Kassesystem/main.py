import wx

import json
import jmespath
import requests
import datetime
import os

logLocation = os.path.expanduser("~\\Documents\\Kassesystem_log\\")
dirname = os.path.dirname(__file__)
productsPath = os.path.join(dirname, "varer.json")
iconPath = os.path.join(dirname, "icon.png")


class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """

    def __init__(self, parent, title, data):
        self.SCREENWIDTH = 1920
        self.SCREENHEIGHT = 800
        self.MARGIN = 4
        self.BUTTONSIZE = 100
        wx.Frame.__init__(self, parent, title=title, size=(
            self.SCREENWIDTH, self.SCREENHEIGHT))

        self.SetIcon(wx.Icon(iconPath))

        self.CreateStatusBar()  # A Statusbar in the bottom of the window
        # Setting up the menu.
        filemenu = wx.Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        self.Bind(wx.EVT_MENU, self.OnAbout,
                  filemenu.Append(wx.ID_ABOUT, "&About",
                                  " Information about this program")
                  )

        filemenu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.OnExit,
                  filemenu.Append(wx.ID_EXIT, "E&xit",
                                  " Terminate the program")
                  )

        # Creating the menubar.
        menuBar = wx.MenuBar()
        # Adding the "filemenu" to the MenuBar
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content

        bigFont = wx.Font(18,  wx.DECORATIVE, wx.NORMAL, wx.NORMAL)

        # Create main panel
        mainPanel = wx.Panel(self)

        mainBox = wx.BoxSizer(wx.HORIZONTAL)

        # Create vertical box for flow
        vbox = wx.BoxSizer(wx.VERTICAL)

        # # Make static box for tickets
        # tickets = wx.StaticBox(mainPanel, -1, "Billetter")

        # # Create StaticBoxSizer for buttons to float in, assigned to StaticBox parent
        # ticktsSizer = wx.StaticBoxSizer(tickets, wx.HORIZONTAL)

        # # Create buttons for StaticBoxSizer
        # for item in data["billetter"]:
        #     product = wx.Button(mainPanel, -1, label=item["name"] + "\n" + str(item["price"]) + " kroner", size=wx.Size(
        #         self.BUTTONSIZE, self.BUTTONSIZE), style=wx.ALIGN_LEFT, name=item["name"])
        #     product.Bind(wx.EVT_BUTTON, self.OnTicket)
        #     ticktsSizer.Add(product, 0, wx.ALL | wx.CENTER, 5)

        # # Add tickets StaticBox to vbox
        # vbox.Add(ticktsSizer, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        ########################################

        for category in data:
            # Create StaticBox for product groups
            group = wx.StaticBox(mainPanel, -1, category["category"])

            # Create StaticBoxSizer for buttons to float in, assigned to StaticBox parent
            groupSizer = wx.StaticBoxSizer(group, wx.HORIZONTAL)

            # Create buttons for StaticBoxSizer
            for item in category["products"]:
                product = wx.Button(mainPanel, -1, size=wx.Size(self.BUTTONSIZE,
                                                                self.BUTTONSIZE), style=wx.ALIGN_LEFT, name=category["category"] + ":" + item["name"])

                label = item["name"]
                if "products" in item:
                    label += "..."
                    product.Bind(wx.EVT_BUTTON, self.OnProductGroup)
                else:
                    label += "\n" + str(item["price"]) + " kroner"
                    product.Bind(wx.EVT_BUTTON, self.OnProduct)

                product.SetLabel(label)

                groupSizer.Add(product, 0, wx.ALL | wx.CENTER, 5)

            vbox.Add(groupSizer, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        andet = wx.Button(mainPanel, label="Andet", size=wx.Size(
            self.BUTTONSIZE, self.BUTTONSIZE))
        andet.Bind(wx.EVT_BUTTON, self.OnOther)
        vbox.Add(andet, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        mainBox.Add(vbox, 0, wx.ALL | wx.ALIGN_TOP, 5)

        rightBox = wx.BoxSizer(wx.VERTICAL)
        wrap = wx.BoxSizer(wx.VERTICAL)

        self.itemList = wx.ListCtrl(mainPanel, size=wx.Size(
            400, self.GetClientSize()[1] - 50), style=wx.LC_REPORT)
        self.itemList.AppendColumn("Vare")
        self.itemList.AppendColumn("Antal")
        self.itemList.AppendColumn("Stykpris")
        self.itemList.AppendColumn("Samlet pris")
        self.itemList.AppendColumn("Moms")
        # self.itemList.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnListChange)

        #                          > < must be 1 for expand
        rightBox.Add(self.itemList, 1, wx.ALL | wx.EXPAND, 5)

        editBox = wx.BoxSizer(wx.HORIZONTAL)

        addButton = wx.Button(mainPanel, label="Tilføj 1")
        addButton.Bind(wx.EVT_BUTTON, self.OnAdd)
        subtractButton = wx.Button(mainPanel, label="Fjern 1")
        subtractButton.Bind(wx.EVT_BUTTON, self.OnSubtract)
        deleteButton = wx.Button(mainPanel, label="Slet række")
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDelete)
        deleteEverythingButton = wx.Button(mainPanel, label="Slet alt")
        deleteEverythingButton.Bind(wx.EVT_BUTTON, self.OnReset)

        editBox.Add(addButton, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        editBox.Add(subtractButton, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        editBox.Add(deleteButton, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        editBox.Add(deleteEverythingButton, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        rightBox.Add(editBox, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        totalBox = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(mainPanel, label="Total")
        text.SetFont(bigFont)

        totalBox.Add(text, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        totalText = wx.TextCtrl(mainPanel, style=wx.TE_READONLY)
        totalText.SetFont(bigFont)
        self.totalText = totalText

        totalBox.Add(totalText, 1, wx.ALL | wx.ALIGN_CENTER, 5)

        rightBox.Add(totalBox, 0, wx.ALL | wx.EXPAND, 5)

        button = wx.Button(mainPanel, label="Betal...", size=wx.Size(400, 100))
        button.SetFont(bigFont)
        button.Bind(wx.EVT_BUTTON, self.OnPay)
        rightBox.Add(button, 0, wx.ALL, 5)

        #rightBox.Add(wx.Button(mainPanel, size=wx.Size(500, 300)), 0, wx.ALL|wx.CENTER, 5)

        #pan = wx.Panel(mainPanel, size=wx.Size(2,100))
        # pan.SetBackgroundColour((32,253,32))

        wrap.Add(rightBox, 1, wx.ALL | wx.ALIGN_RIGHT)

        # rightBox.Add(pan)

        mainBox.Add(wrap, 1, wx.EXPAND)

        mainPanel.SetSizer(mainBox)

        self.Show(True)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(
            self, "Dette er Hedelands Veteranbanes kassesystem", "Om kassesystemet")
        print(self.GetSize())
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        # Gem alt der skal gemmes
        self.Close(True)

    def AddToBasket(self, item):
        print("/\\/\\/\\/\\/\\/\\")
        print(item)
        # Tjek om produktet allerede er på listen
        index = self.itemList.FindItem(-1, item["name"])
        if index != -1 and self.itemList.GetItem(index, col=2).GetText() == str(item["price"]):
            #print(self.itemList.GetItem(index, col=2).GetText())
            # Get rowcolumn
            rowcol = self.itemList.GetItem(index, col=1)
            # Get value of rowcol, antal
            itemCount = rowcol.GetText()
            itemCountNew = int(itemCount) + 1
            self.itemList.SetItem(index, 1, str(itemCountNew), imageId=-1)
            # Recalculate samlet pris
            self.itemList.SetItem(index, 3, str(
                itemCountNew * int(item["price"])), imageId=-1)
        else:
            if "moms" not in item:
                item.update({"moms": 25})
            self.itemList.Append(
                [item["name"], "1", item["price"], item["price"], item["moms"]])
            print([item["name"], "1", item["price"], item["price"], item["moms"]])

        self.OnListChange(None)

    def OnProductGroup(self, event):
        category, productName = event.GetEventObject().GetName().split(":")
        print("[?category=='" + category +
              "'].[products][][?name=='" + productName + "']")
        group = jmespath.search(
            "[?category=='" + category + "'].[products][][?name=='" + productName + "']", data)[0][0]
        print(group)
        opengroup = itemChoose(self, "Varegruppen \"" +
                               group["name"] + "\"", group)

    def OnProduct(self, event):
        category, productName = event.GetEventObject().GetName().split(":")
        item = jmespath.search(
            "[?category=='" + category + "'].[products][][?name=='" + productName + "']", data)[0][0]
        # item = jmespath.search(
        #    "[*].products[?name=='" + productName + "']", data)[0]
        # print(jmespath.search(
        #    "[*].products[?name=='" + productName + "']", data))
        self.AddToBasket(item)

    def OnTicket(self, event):
        item = jmespath.search(
            "billetter[?name=="" + event.GetEventObject().GetName() + ""]", data)[0]
        self.AddToBasket(item)

    def OnAdd(self, event):
        index = self.itemList.GetFirstSelected()

        # Get rowcolumn
        rowcol = self.itemList.GetItem(index, col=1)
        itemCount = rowcol.GetText()
        itemCountNew = int(itemCount) + 1
        self.itemList.SetItem(index, 1, str(itemCountNew), imageId=-1)

        rowcol = self.itemList.GetItem(index, col=2)
        price = int(rowcol.GetText())

        # Recalculate samlet pris
        self.itemList.SetItem(index, 3, str(itemCountNew * price), imageId=-1)
        self.OnListChange(event)

    def OnSubtract(self, event):
        index = self.itemList.GetFirstSelected()

        # Get rowcolumn
        rowcol = self.itemList.GetItem(index, col=1)
        itemCount = int(rowcol.GetText())

        if(itemCount <= 1):

            self.OnDelete(None)
            return

        itemCountNew = itemCount - 1
        self.itemList.SetItem(index, 1, str(itemCountNew), imageId=-1)

        rowcol = self.itemList.GetItem(index, col=2)
        price = int(rowcol.GetText())

        # Recalculate samlet pris
        self.itemList.SetItem(index, 3, str(itemCountNew * price), imageId=-1)
        self.OnListChange(event)

    def OnDelete(self, event):
        index = self.itemList.GetFirstSelected()
        self.itemList.DeleteItem(index)
        self.OnListChange(event)

    def OnPay(self, event):
        columns = []
        for i in range(0, self.itemList.GetColumnCount()):
            columns.append(self.itemList.GetColumn(i).GetText())

        rows = []
        for i in range(0, self.itemList.GetItemCount()):
            row = {}
            for j in range(0, len(columns)):
                row.update({columns[j]: self.itemList.GetItem(i, j).GetText()})
            rows.append(row)

        print(rows)
        paymentChoose(self, rows)

    def OnOther(self, event):
        other(self)

    def OnListChange(self, event):
        columns = []
        for i in range(0, self.itemList.GetColumnCount()):
            columns.append(self.itemList.GetColumn(i).GetText())

        total = 0
        for i in range(0, self.itemList.GetItemCount()):
            total += float(self.itemList.GetItem(i,
                                                 columns.index("Samlet pris")).GetText())
            self.totalText.SetValue(str(total))

    def OnReset(self, event):
        self.Reset()

    def Reset(self):
        self.itemList.DeleteAllItems()
        self.totalText.SetValue("0")


class itemChoose(wx.Frame):
    """ We simply derive a new class of Frame. """

    def __init__(self, parent, title, data):
        self.SCREENWIDTH = 800
        self.SCREENHEIGHT = 800
        self.MARGIN = 4
        self.BUTTONSIZE = 100
        self.data = data
        self.chooseMultiple = False
        wx.Frame.__init__(self, parent, title=title, size=(self.SCREENWIDTH, self.SCREENHEIGHT), pos=wx.Point(
            50, 50), style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)

        mainPanel = wx.Panel(self)

        mainBox = wx.BoxSizer(wx.VERTICAL)

        products = wx.StaticBox(mainPanel, -1, "Varegrupper")
        productsSizer = wx.StaticBoxSizer(products, wx.HORIZONTAL)

        gs = wx.GridSizer((800 - self.BUTTONSIZE)/self.BUTTONSIZE,
                          (800 - self.BUTTONSIZE)/self.BUTTONSIZE, 5, 5)

        for item in data["products"]:
            product = wx.Button(mainPanel, -1, size=wx.Size(self.BUTTONSIZE, self.BUTTONSIZE), style=wx.ALIGN_LEFT,
                                name=item["name"], label=item["name"] + "\n" + str(item["price"]) + " kroner")
            product.Bind(wx.EVT_BUTTON, self.OnProduct)
            gs.Add(product, 0, wx.EXPAND)

        productsSizer.Add(gs, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        mainBox.Add(productsSizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_TOP, 5)

        self.cancelButton = wx.Button(mainPanel, -1, label="Annullér")
        self.cancelButton.Bind(
            wx.EVT_BUTTON, self.OnButton
        )

        multiple = wx.CheckBox(mainPanel, label="Vælg flere")
        multiple.Bind(wx.EVT_CHECKBOX, self.OnChecked)

        bottomBox = wx.BoxSizer(wx.HORIZONTAL)
        bottomBox.Add(multiple, 0, wx.ALL | wx.ALIGN_RIGHT |
                      wx.ALIGN_CENTER_VERTICAL, 5)
        bottomBox.Add(self.cancelButton, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        mainBox.Add(bottomBox, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        mainPanel.SetSizer(mainBox)
        self.Show(True)

    def OnProduct(self, event):
        item = jmespath.search(
            "products[?name=='" + event.GetEventObject().GetName() + "']", self.data)[0]
        frame.AddToBasket(item)
        if not self.chooseMultiple:
            self.Close(True)

    def OnButton(self, event):
        self.Close(True)

    def OnChecked(self, event):
        self.chooseMultiple = event.GetEventObject().GetValue()
        if self.chooseMultiple == True:
            self.cancelButton.SetLabel("Afslut")
        else:
            self.cancelButton.SetLabel("Annullér")


class other(wx.Frame):
    """ We simply derive a new class of Frame. """

    def __init__(self, parent):
        self.SCREENWIDTH = 400
        self.SCREENHEIGHT = 200
        self.data = data
        self.parent = parent
        wx.Frame.__init__(self, parent, title="Anden vare", size=(self.SCREENWIDTH, self.SCREENHEIGHT), pos=wx.Point(
            50, 50), style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)

        mainPanel = wx.Panel(self)

        mainBox = wx.BoxSizer(wx.HORIZONTAL)

        productBox = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(mainPanel, label="Varenavn")
        self.productName = wx.TextCtrl(mainPanel, value="Andet")
        productBox.Add(label, 0, wx.ALL, 5)
        productBox.Add(self.productName, 0, wx.ALL, 5)
        mainBox.Add(productBox, 0, wx.ALL, 5)

        productBox = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(mainPanel, label="Stykpris")
        self.productPrice = wx.TextCtrl(mainPanel, value="0")
        productBox.Add(label, 0, wx.ALL, 5)
        productBox.Add(self.productPrice, 0, wx.ALL, 5)
        mainBox.Add(productBox, 0, wx.ALL, 5)

        button = wx.Button(mainPanel, label="Tilføj")
        button.Bind(wx.EVT_BUTTON, self.OnDone)
        mainBox.Add(button, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)

        mainPanel.SetSizer(mainBox)

        self.Show(True)

    def OnDone(self, event):
        name = self.productName.GetValue()
        price = self.productPrice.GetValue()
        try:
            price = float(price.replace(",", "."))
        except ValueError:
            wx.MessageBox("Ugyldig pris!", "Error", wx.OK | wx.ICON_ERROR)
            return
        frame.AddToBasket({"name": name, "price": price})
        self.Close(True)


class paymentChoose(wx.Frame):
    """ We simply derive a new class of Frame. """

    def __init__(self, parent, data):
        self.SCREENWIDTH = 400
        self.SCREENHEIGHT = 200
        self.data = data
        self.parent = parent
        wx.Frame.__init__(self, parent, title="Betalingsvalg", size=(self.SCREENWIDTH, self.SCREENHEIGHT), pos=wx.Point(
            50, 50), style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)

        mainPanel = wx.Panel(self)

        mainBox = wx.BoxSizer(wx.HORIZONTAL)

        button = wx.Button(mainPanel, label="Kontant", name="Kontant")
        button.Bind(wx.EVT_BUTTON, self.OnChoose)
        mainBox.Add(button, 0, wx.ALL | wx.EXPAND, 5)

        button = wx.Button(mainPanel, label="MobilePay", name="MobilePay")
        button.Bind(wx.EVT_BUTTON, self.OnChoose)
        mainBox.Add(button, 0, wx.ALL | wx.EXPAND, 5)

        mainPanel.SetSizer(mainBox)

        self.Show(True)

    def OnChoose(self, event):
        os.makedirs(os.path.dirname(logLocation), exist_ok=True)

        with open(logLocation + "\\" + datetime.datetime.today().strftime("%d-%m-%Y") + ".json", "a") as file:
            file.write(json.dumps({"date": datetime.datetime.today().strftime(
                "%d-%m-%Y %H:%M:%S"), "paymentMethod": event.GetEventObject().GetName(), "receipt": self.data}) + "\n")
        try:
            requests.post("http://localhost:9100", json=self.data)
        except:
            wx.MessageBox("Kunne ikke forbinde til printeren",
                          "Warning", wx.OK | wx.ICON_WARNING)
        frame.Reset()
        self.Close(True)


app = wx.App(False)

with open(productsPath, encoding="utf-8") as json_file:
    data = json.load(json_file)

frame = MyFrame(None, "Hedelands Veteranbane - Kassesystem", data)
app.MainLoop()
