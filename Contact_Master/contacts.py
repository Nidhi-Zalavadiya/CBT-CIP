from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
import db

# Set a bright color scheme for the app
Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Light gray background

class ContactMasterApp(App):
    def build(self):
        db.Initialization()
        self.contacts = []
        self.main_layout = FloatLayout()

        # Search layout
        self.search_layout = GridLayout(cols=3, padding=10, spacing=10, size_hint=(0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.9}, row_default_height=40)
        self.search_input = TextInput(hint_text='Search by Name or Phone', multiline=False, size_hint_y=None, height=40, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        search_button = Button(text='Search', size_hint_y=None, height=40, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        search_button.bind(on_press=self.search_contact)
        view_all_button = Button(text='View All Contacts', size_hint_y=None, height=40, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        view_all_button.bind(on_press=self.view_all_contacts)

        self.search_layout.add_widget(self.search_input)
        self.search_layout.add_widget(search_button)
        self.search_layout.add_widget(view_all_button)

        # Form layout
        self.form_layout = GridLayout(cols=2, padding=20, spacing=15, size_hint=(0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, row_default_height=40)
        self.name_input = TextInput(hint_text='Name', multiline=False, size_hint_y=None, height=40, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.phone_input = TextInput(hint_text='Phone Number', multiline=False, size_hint_y=None, height=40, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.email_input = TextInput(hint_text='Email', multiline=False, size_hint_y=None, height=40, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        self.form_layout.add_widget(Label(text='Name:', size_hint_x=None, width=150, color=(0, 0, 0, 1)))
        self.form_layout.add_widget(self.name_input)
        self.form_layout.add_widget(Label(text='Phone Number:', size_hint_x=None, width=150, color=(0, 0, 0, 1)))
        self.form_layout.add_widget(self.phone_input)
        self.form_layout.add_widget(Label(text='Email:', size_hint_x=None, width=150, color=(0, 0, 0, 1)))
        self.form_layout.add_widget(self.email_input)

        add_button = Button(text='Add Contact', size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        add_button.bind(on_press=self.add_contact)
        self.form_layout.add_widget(add_button)

        # Contact list layout (for internal use)
        self.contact_list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.contact_list_layout.bind(minimum_height=self.contact_list_layout.setter('height'))

        # Add widgets to the main layout
        self.main_layout.add_widget(self.search_layout)
        self.main_layout.add_widget(self.form_layout)

        return self.main_layout

    def add_contact(self, instance):
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()
        email = self.email_input.text.strip()

        if not name or not phone:
            self.show_message("Name and Phone Number are required!")
            return

        if not self.validate_phone(phone):
            self.show_message("Invalid Phone Number!")
            return

        

        if email and not self.validate_email(email):
            self.show_message("Invalid Email Address!")
            return

        # Check for duplicate contact
        if db.get_one_contact(name) or db.get_one_contact(phone) or (email and db.get_one_contact(email)):
            self.show_message("Contact with this Name, Phone Number, or Email already exists!")
            return

        db.add_contact(name=name, phone=phone, email=email)
        self.show_contact_details_popup(name, phone, email)

        # Clear inputs
        self.name_input.text = ''
        self.phone_input.text = ''
        self.email_input.text = ''

    def show_contact_details_popup(self, name, phone, email):
        layout = BoxLayout(orientation='vertical', padding=10)
        contact_details = f'Name: {name}\nPhone Number: {phone}\nEmail: {email}'
        details_label = Label(text=contact_details, size_hint_y=None, height=40)
        back_button = Button(text='Back', size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        back_button.bind(on_press=self.close_popup)
        
        layout.add_widget(details_label)
        layout.add_widget(back_button)

        self.popup = Popup(title='Contact Details', content=layout, size_hint=(0.6, 0.4), background_color=(1, 1, 1, 1))  # Bright popup background
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

    def view_all_contacts(self, instance):
        self.display_contacts_in_popup(db.get_all_contacts(), title="All Contacts")

    def search_contact(self, instance):
        query = self.search_input.text.strip()
        if not query:
            self.show_message("Search query cannot be empty!")
            return

        results = db.get_one_contact(query)
        if results:
            self.display_contacts_in_popup(results, title="Search Results")
        else:
            self.show_message("No contacts found")
        
        self.search_input.text = ''

    def display_contacts_in_popup(self, contacts, title="Contacts"):
        layout = BoxLayout(orientation='vertical', padding=10)
        contact_list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        contact_list_layout.bind(minimum_height=contact_list_layout.setter('height'))

        for contact in contacts:
            contact_label = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            contact_info = Label(text=f'{contact[1]} - {contact[2]} - {contact[3]}', size_hint_x=0.7)
            edit_button = Button(text='Edit', size_hint_x=0.15)
            delete_button = Button(text='Delete', size_hint_x=0.15)

            edit_button.bind(on_press=self.edit_contact)
            delete_button.bind(on_press=self.delete_contact)

            contact_label.add_widget(contact_info)
            contact_label.add_widget(edit_button)
            contact_label.add_widget(delete_button)

            contact_list_layout.add_widget(contact_label)
        
        scroll_view = ScrollView(size_hint=(1, 1), size=(600, 400))
        scroll_view.add_widget(contact_list_layout)

        back_button = Button(text='Back', size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        back_button.bind(on_press=self.close_popup)

        layout.add_widget(scroll_view)
        layout.add_widget(back_button)

        self.popup = Popup(title=title, content=layout, size_hint=(0.8, 0.6), background_color=(1, 1, 1, 1))  # Bright popup background
        self.popup.open()

    def show_contact_details(self, instance):
        details = instance.text.split(' - ')
        if len(details) >= 3:
            name, phone, email = details
            self.show_contact_details_popup(name, phone, email)

    def edit_contact(self, instance):
        contact_info = instance.parent.children[2].text.split(' - ')
        if len(contact_info) >= 3:
            name, phone, email = contact_info
            old_name = name 
            self.show_edit_contact_popup(old_name,name, phone, email)

    def delete_contact(self, instance):
        contact_info = instance.parent.children[2].text.split(' - ')
        if len(contact_info) >= 3:
            name, phone, email = contact_info
            db.delete_contact(name=name, phone=phone, email=email)
            self.show_message(f"Contact '{name}' deleted!")
            self.view_all_contacts(None)

    def show_edit_contact_popup(self, old_name, name, phone, email):
        layout = GridLayout(cols=2, padding=10, spacing=10)
        name_input = TextInput(text=name, multiline=False, size_hint_y=None, height=40, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        phone_input = TextInput(text=phone, multiline=False, size_hint_y=None, height=40, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        email_input = TextInput(text=email, multiline=False, size_hint_y=None, height=40, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        layout.add_widget(Label(text='Name:', size_hint_x=None, width=150, color=(0, 0, 0, 1)))
        layout.add_widget(name_input)
        layout.add_widget(Label(text='Phone Number:', size_hint_x=None, width=150, color=(0, 0, 0, 1)))
        layout.add_widget(phone_input)
        layout.add_widget(Label(text='Email:', size_hint_x=None, width=150, color=(0, 0, 0, 1)))
        layout.add_widget(email_input)

        save_button = Button(text='Save Changes', size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        save_button.bind(on_press=lambda btn: self.save_changes(old_name, name_input.text, phone_input.text, email_input.text))
        layout.add_widget(save_button)

        back_button = Button(text='Back', size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        back_button.bind(on_press=self.close_popup)
        layout.add_widget(back_button)

        self.popup = Popup(title='Edit Contact', content=layout, size_hint=(0.8, 0.6), background_color=(1, 1, 1, 1))  # Bright popup background
        self.popup.open()

    def save_changes(self, old_name, new_name, new_phone, new_email):
        # Add validation and update logic here
        if not new_name or not new_phone:
            self.show_message("Name and Phone Number are required!")
            return

        if not self.validate_phone(new_phone):
            self.show_message("Invalid Phone Number!")
            return

        if new_email and not self.validate_email(new_email):
            self.show_message("Invalid Email Address!")
            return

        try:
            db.update_contact(old_name, new_name, new_phone, new_email)  # Ensure this function is implemented in your `db` module
            self.show_message("Contact updated successfully!")
        except Exception as e:
            self.show_message(f"An error occurred: {str(e)}")
        finally:
            self.close_popup(None)
            self.view_all_contacts(None)

    def validate_phone(self, phone):
        import re
        pattern = re.compile(r'^\+?\d{10,15}$')
        return pattern.match(phone) is not None

    def validate_email(self, email):
        import re
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return pattern.match(email) is not None

    def show_message(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(0.6, 0.3), background_color=(1, 1, 1, 1))  # Bright popup background
        popup.open()

if __name__ == '__main__':
    ContactMasterApp().run()
