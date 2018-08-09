# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
from kivy.network.urlrequest import UrlRequest
import urllib
import json
import os

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem


NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "Navigation Drawer"
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Home"
            on_release: app.root.ids.scr_mngr.current = 'accordion'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Profile"
            on_release: app.root.ids.scr_mngr.current = 'bottom_navigation'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "About"
            on_release: app.root.ids.scr_mngr.current = 'bottom_navigation'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Contact"
            on_release: app.root.ids.scr_mngr.current = 'bottom_navigation'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Logout"
            on_release: app.user_logout()
    BoxLayout:
        orientation: 'vertical'
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'user_login'

                Toolbar:
                    title: "User Login"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.95}
                    md_bg_color: app.theme_cls.primary_color
                    background_palette: 'Primary'
                    background_hue: '500'
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: None
                    size_hint_y: None
                    pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                    width: dp(500)
                    BoxLayout:
                        orientation: 'vertical'
                        MDTextField:
                            id: email
                            hint_text: "Email"
                            margin_bottom: dp(20)
                            required: True
                            helper_text_mode: "on_error"

                        MDTextField:
                            id: password
                            hint_text: "Password"
                            margin_bottom: dp(20)
                            required: True
                            helper_text_mode: "on_error"
                            password: True

                        MDRaisedButton:
                            id: login
                            text: "Sign in"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                            on_release:  app.user_login()
                            on_press: app.progress_loader('login')
                        MDSpinner:
                            id: spinner_login
                            size_hint: None, None
                            size: dp(50), dp(50)
                            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                            active: False
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        MDFlatButton:
                            id: forgot_password
                            text: 'Forgot Password'
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            on_release:  app.root.ids.scr_mngr.current = 'forgot_password'

                        MDFlatButton:
                            id: register
                            text: 'Register'
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            on_release:  app.root.ids.scr_mngr.current = 'register'


            Screen:
                name: 'forgot_password'
                Toolbar:
                    title: "Forgot Password"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.95}
                    md_bg_color: app.theme_cls.primary_color
                    background_palette: 'Primary'
                    background_hue: '500'
                    left_action_items: [['arrow-left', lambda x: app.back_to_login()]]


            Screen:
                name: 'user_home'
                Toolbar:
                    title: "Home"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.95}
                    md_bg_color: app.theme_cls.primary_color
                    background_palette: 'Primary'
                    background_hue: '500'
                    left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]



            Screen:
                name: 'register'
                Toolbar:
                    title: "Register"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.95}
                    md_bg_color: app.theme_cls.primary_color
                    background_palette: 'Primary'
                    background_hue: '500'
                    left_action_items: [['arrow-left', lambda x: app.back_to_login()]]
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: None
                    size_hint_y: None
                    pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                    width: dp(500)
                    BoxLayout:
                        orientation: 'vertical'
                        MDTextField:
                            id: first_name
                            hint_text: "First Name(Optional)"
                            margin_bottom: dp(20)
                            required: True
                            helper_text_mode: "on_error"
                        MDTextField:
                            id: last_name
                            hint_text: "Last Name(Optional)"
                            margin_bottom: dp(20)
                            required: True
                            helper_text_mode: "on_error"
                        MDTextField:
                            id: email_signup
                            hint_text: "Email"
                            margin_bottom: dp(20)
                            required: True
                            helper_text_mode: "on_error"
                        MDTextField:
                            id: password_signup
                            hint_text: "Password"
                            margin_bottom: dp(20)
                            required: True
                            helper_text_mode: "on_error"
                            password: True
                        MDRaisedButton:
                            id: signup
                            text: "Sign up"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            on_release:  app.user_register()
                            on_press: app.progress_loader('register')
                        MDSpinner:
                            id: spinner_register
                            size_hint: None, None
                            size: dp(50), dp(50)
                            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                            active: False

            Screen:
                name: 'verify_email'
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: None
                    size_hint_y: None
                    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                    width: dp(500)
                    BoxLayout:
                        orientation: 'vertical'
                        MDTextField:
                            id: email_verify
                            hint_text: "Paste Verification Code"
                            margin_bottom: dp(20)
                            required: True
                            helper_text_mode: "on_error"
                        MDRaisedButton:
                            id: verify
                            text: "Verify"
                            elevation_normal: 2
                            opposite_colors: True
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            on_release:  app.user_verify_email()
                            on_press: app.progress_loader('verify')
                        MDSpinner:
                            id: spinner_verify
                            size_hint: None, None
                            size: dp(50), dp(50)
                            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                            active: False


'''
HOST_URL = 'http://userauth.pythonanywhere.com/'


class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)


class UserAuthApp(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "User Authentication App"
    menu_items = [
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
    ]

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        if os.stat("token.json").st_size != 0:
            with open('token.json') as f:
                data = json.load(f)
                result = data['token']
                token = 'Token ' + result
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'Authorization': token}
                req = UrlRequest(HOST_URL+'api/accounts/users/me/', method='GET',
                                 on_success=self.user_home_welcome,
                                 on_failure=self.user_login, req_headers=headers)
        else:
            self.user_login
        return main_widget

    def user_login(self, *args):
        email = self.root.ids.email.text
        password = self.root.ids.password.text

        '''if email == '':
            content = MDLabel(font_style='Body1',
                              theme_text_color='Secondary',
                              text='please input email and password',
                              size_hint_y=None,
                              valign='top')
            content.bind(texture_size=content.setter('size'))
            self.dialog = MDDialog(title="Fields cannot be empty",
                                   content=content,
                                   size_hint=(.8, None),
                                   height=dp(200),
                                   auto_dismiss=False)

            self.dialog.add_action_button("Login",
                                          action=lambda *x: self.dialog.dismiss())
            self.dialog.open()
        else:'''
        if email != '':
            params = json.dumps({'email': email, 'password': password})
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}
            req = UrlRequest(HOST_URL+'api/accounts/login/', method='POST', on_success=self.user_home_welcome, on_failure=self.user_login_error, req_body=params,
                             req_headers=headers)

    def user_register(self, *args):
        first_name = self.root.ids.first_name.text
        last_name = self.root.ids.last_name.text
        email = self.root.ids.email_signup.text
        password = self.root.ids.password_signup.text

        params = json.dumps({'email': email, 'password': password, 'first_name': first_name, 'last_name': last_name})
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}
        req = UrlRequest(HOST_URL+'api/accounts/signup/', method='POST', on_success=self.user_verify_email,
                         on_failure=self.user_register_error, req_body=params,
                         req_headers=headers)

    def user_verify_email(self, *args):
        self.root.ids.scr_mngr.current = 'verify_email'
        code = self.root.ids.email_verify.text
        if code != '':
            headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}
            req = UrlRequest(HOST_URL+'api/accounts/signup/verify/?code='+code, method='GET', on_success=self.user_home_welcome,
                             on_failure=self.user_verify_error,
                             req_headers=headers)

    def user_home_welcome(self, result, req):
        result = req['token']
        if os.stat("token.json").st_size == 0:
            with open('token.json', 'w') as outfile:
                json.dump(result, outfile)
        self.root.ids.spinner_verify.active = False
        self.root.ids.spinner_login.active = False
        self.root.ids.scr_mngr.current = 'user_home'

    def user_login_error(self, *args):
        self.root.ids.scr_mngr.current = 'user_login'
        self.root.ids.spinner_login.active = False
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text='Unable to login with provided credentials',
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Please check email and password",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Try Again",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def user_register_error(self, req, result):
        self.root.ids.spinner_register.active = False
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text='Check details entered again',
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Registration Failed",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Try Again",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def user_verify_error(self, req, result):
        self.root.ids.spinner_verify.active = False
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text='Invalid or empty code',
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Please enter the code sent to your email correctly",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Try Again",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def back_to_login(self):
        self.root.ids.scr_mngr.current = 'user_login'

    def back_to_signup(self):
        self.root.ids.spinner_register.active = False
        self.root.ids.scr_mngr.current = 'register'

    def progress_loader(self, screen):
        if screen == 'register':
            self.root.ids.spinner_register.active = True
        elif screen == 'verify':
            self.root.ids.spinner_verify.active = True
        elif screen == 'login':
            self.root.ids.spinner_login.active = True

    def user_logout(self):
        f = open('token.json', 'r+')
        f.truncate(0)
        self.root.ids.scr_mngr.current = 'user_login'

    def on_pause(self):
        return True

    def on_stop(self):
        pass


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


if __name__ == '__main__':
    UserAuthApp().run()
