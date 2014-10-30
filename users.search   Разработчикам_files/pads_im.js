var PadsIm = {
  init: function() {
    if (!_pads.content) return;

    var id = 'msg', titleH = ge('pad_title_wrap').offsetHeight;
    var dy = getXY(ge('l_' + id), true)[1] - 40 + titleH;
    var padH = 540 - titleH - ge('pad_footer_wrap').offsetHeight;
    extend(_pads.cur, {
      dialogs: ge('pad_im_drows'),
      history: ge('pad_im_hrows')
    });
    setStyle(_pads.cont, {
      width: 644,
      height: 540
    });
    setStyle(_pads.cur.dialogs, {
      height: padH
    });
    setStyle(_pads.cur.history, {
      height: padH
    });
    setStyle(_pads.wrap, {
      top: (getXY(ge('l_' + id), true)[1] - dy)
    });
    hide('pad_arrow');

    var scrollOpts = {
      prefix: 'pad_',
      nomargin: true,
      global: true,
      nokeys: true,
      right: vk.rtl ? 'auto' : 1,
      left: !vk.rtl ? 'auto' : 1
    };

    _pads.scroll = new Scrollbar(_pads.cur.dialogs, extend({wheelObj: _pads.cur.dialogs}, scrollOpts));
    _pads.cur.dialogs.onscroll = PadsIm.dialogsScroll;
    _pads.scroll.scrollTop(0);

    _pads.scrollHistory = new Scrollbar(_pads.cur.history, extend({wheelObj: _pads.cur.history}, scrollOpts));
    _pads.cur.history.onscroll = PadsIm.historyScroll;
    _pads.scrollHistory.scrollTop(_pads.cur.history.scrollHeight);
  },
  destroy: function() {
    setStyle(_pads.cont, {height: ''});
  }
};

try {stManager.done('pads_im.js')}catch(e){}