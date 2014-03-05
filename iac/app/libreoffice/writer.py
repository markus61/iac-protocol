from uno import getComponentContext
from com.sun.star.connection import ConnectionSetupException
from com.sun.star.awt.FontWeight import BOLD
import sys

# For saving the file
from com.sun.star.beans import PropertyValue    
from uno import systemPathToFileUrl


class Message(object):
    connection_setup_exception = "Error: Please start the uno bridge first."


# Connect to libreoffice using UNO
UNO_PORT = 18101
try:
    localContext = getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", localContext)
    context = resolver.resolve(
            "uno:socket,host=localhost,port=%d;urp;StarOffice.ComponentContext" % UNO_PORT)
except ConnectionSetupException:
    print("%s\n" % Message.connection_setup_exception)
    sys.exit(1)

# Get the desktop service
desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)


class Interface(object):
    variables = {}

    @staticmethod
    def current_document():
        """current_document()"""
        return desktop.getCurrentComponent()

    @staticmethod
    def load_document(path):
        """load_document(['path'])"""
        url = systemPathToFileUrl(path)
        return desktop.loadComponentFromURL(url ,"_blank", 0, ())

    @staticmethod
    def new_document():
        """new_document()"""
        return desktop.loadComponentFromURL("private:factory/swriter","_blank", 0, ())

    @staticmethod
    def save_as(document, path):
        """[document].save_as(['path'])"""
        url = systemPathToFileUrl(path)

        # Set file to overwrite
        property_value = PropertyValue()
        property_value.Name = 'Overwrite'
        property_value.Value = 'overwrite'
        properties = (property_value,)

        # Save to file
        document.storeAsURL(url, properties)
        return True

    @staticmethod
    def save_as_pdf(document, path):
        """[document].save_as_pdf(['path'])"""
        url = systemPathToFileUrl(path)

        # Set file type to pdf
        property_value = PropertyValue()
        property_value.Name = 'FilterName'
        property_value.Value = 'writer_pdf_Export'

        properties = (property_value,)

        # Store file
        document.storeToURL(url, properties)
        return True

    @staticmethod
    def select_text(document):
        """[document].select_text()"""
        xSelectionSupplier = document.getCurrentController()
        xIndexAccess = xSelectionSupplier.getSelection() 
        return xIndexAccess.getByIndex(0)

    @staticmethod
    def get_text(text_range):
        """[text_range].get_text()"""
        return text_range.getString()

    @staticmethod
    def weight(text_range, bold):
        """[text_range].weight(['bold'])"""
        if bold.strip("'").strip('"') == "bold":
            text_range.CharWeight = BOLD
            return True
        else:
            return False
