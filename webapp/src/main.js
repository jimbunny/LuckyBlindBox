import Vue from 'vue'
import md5 from 'js-md5';
import App from './App.vue'
import router from './router'
import store from './store'
import { prefix } from '@/common/js/utils'
import LuckDraw from 'vue-luck-draw'
import FBSignInButton from 'vue-facebook-signin-button'
import SlideVerify from 'vue-monoplasty-slide-verify'
import VueClipboard from 'vue-clipboard2'
import { Divider, Popup, Overlay, Loading, Dialog, ContactCard, Form, AddressEdit, AddressList, Field, CellGroup, Cell, SwipeCell, Icon, Stepper, Card, Checkbox, CheckboxGroup, Button, Swipe, SwipeItem, PullRefresh, List, Tab, Tabs, GoodsAction, GoodsActionIcon, 
  GoodsActionButton, SubmitBar, Toast, DropdownMenu, DropdownItem, Switch, Col, Row, Tag, Image as VanImage, ShareSheet, Lazyload, CountDown, RadioGroup, Radio, Calendar, PasswordInput, NumberKeyboard, DatetimePicker, Uploader, Collapse, CollapseItem, Search,
   ActionSheet, Picker, Badge, CouponCell, CouponList, Sticky } from 'vant'
import 'lib-flexible/flexible'

Vue.use(Divider).use(Popup).use(Overlay).use(Loading).use(Dialog).use(Toast).use(ContactCard).use(Form).use(AddressEdit).use(AddressList).use(Field).use(CellGroup).use(Cell).use(SwipeCell).use(Icon).use(Stepper).use(Card).use(Button).use(Swipe).use(SwipeItem).use(PullRefresh).use(List).use(Tab).use(Tabs)
.use(GoodsAction).use(GoodsActionIcon).use(GoodsActionButton).use(SubmitBar).use(Checkbox).use(CheckboxGroup).use(DropdownMenu).use(DropdownItem).use(Switch).use(LuckDraw).use(Row).use(Col).use(Tag).use(VanImage).use(ShareSheet).use(Lazyload).use(CountDown).use(FBSignInButton).use(SlideVerify)
.use(RadioGroup).use(Radio).use(Calendar).use(RadioGroup).use(PasswordInput).use(NumberKeyboard).use(DatetimePicker).use(VueClipboard).use(Uploader).use(Collapse).use(CollapseItem).use(Search).use(ActionSheet).use(Picker).use(Badge).use(CouponCell).use(CouponList).use(Sticky)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

Vue.prototype.$md5 = md5;
Vue.prototype.prefix = prefix;

Array.prototype.remove = function(val) {
  var index = this.indexOf(val);
  if (index > -1) {
    this.splice(index, 1);
  }
}
