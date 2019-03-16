
// namespace
window.semantic = {
  handler: {}
};

// Allow for console.log to not break IE
if (typeof window.console == "undefined" || typeof window.console.log == "undefined") {
  window.console = {
    log  : function() {},
    info : function(){},
    warn : function(){}
  };
}
if(typeof window.console.group == 'undefined' || typeof window.console.groupEnd == 'undefined' || typeof window.console.groupCollapsed == 'undefined') {
  window.console.group = function(){};
  window.console.groupEnd = function(){};
  window.console.groupCollapsed = function(){};
}
if(typeof window.console.markTimeline == 'undefined') {
  window.console.markTimeline = function(){};
}
window.console.clear = function(){};

// ready event
semantic.ready = function() {

  // selector cache
  var
    $document            = $(document),
    $sortableTables      = $('.sortable.table'),
    $sticky              = $('.ui.sticky'),
    $tocSticky           = $('.toc .ui.sticky'),

    $themeDropdown       = $('.theme.dropdown'),

    $ui                  = $('.ui').not('.hover, .down'),
    $swap                = $('.theme.menu .item'),
    $menu                = $('#toc'),
    $hideMenu            = $('#toc .hide.item'),
    $search              = $('#search'),
    $sortTable           = $('.sortable.table'),
    $demo                = $('.demo'),

    $fullHeightContainer = $('.pusher > .full.height'),
    $container           = $('.main.container'),
    $allHeaders          = $('.main.container > h2, .main.container > .tab > h2, .main.container > .tab > .examples h2'),
    $sectionHeaders      = $container.children('h2'),
    $followMenu          = $container.find('.following.menu'),
    $sectionExample      = $container.find('.example'),
    $exampleHeaders      = $sectionExample.children('h4'),
    $footer              = $('.page > .footer'),

    $menuMusic           = $('.ui.main.menu .music.item'),
    $menuPopup           = $('.ui.main.menu .popup.item'),
    $pageDropdown        = $('.ui.main.menu .page.dropdown'),
    $pageTabs            = $('.masthead.tab.segment .tabs.menu .item'),

    $languageDropdown    = $('.language.dropdown'),
    $chineseModal        = $('.chinese.modal'),
    $languageModal       = $('.language.modal'),

    $downloadPopup       = $('.download.button'),
    $downloads           = $('.download.popup'),
    $downloadFramework   = $('.framework.column .button'),
    $downloadInput       = $('.download.popup input'),
    $downloadStandalone  = $('.standalone.column .button'),

    $helpPopup           = $('.header .help'),

    $example             = $('.example'),
    $popupExample        = $example.not('.no'),
    $shownExample        = $example.filter('.shown'),
    $prerenderedExample  = $example.has('.ui.checkbox, .ui.dropdown, .ui.search, .ui.progress, .ui.rating, .ui.dimmer, .ui.embed'),

    $visibilityExample   = $example.filter('.visiblity').find('.overlay, .demo.segment, .items img'),


    $sidebarButton       = $('.fixed.launch.button'),
    $code                = $('div.code').not('.existing'),
    $existingCode        = $('.existing.code'),

    expertiseLevel       = ($.cookie !== undefined)
      ? $.cookie('expertiseLevel') || 0
      : 0,
    languageDropdownUsed = false,

    metadata,

    requestAnimationFrame = window.requestAnimationFrame
      || window.mozRequestAnimationFrame
      || window.webkitRequestAnimationFrame
      || window.msRequestAnimationFrame
      || function(callback) { setTimeout(callback, 0); },

    // alias
    handler
  ;
    handler = {};
};


// attach ready event
$(document)
  .ready(semantic.ready)
;
