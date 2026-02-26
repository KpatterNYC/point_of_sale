const dash_ul = $("#dash-ul");
const path_obj = JSON.parse($("#paths").text());
const menu_btn=$("#menu-btn");
const menu_div=$("#menu-div");
const close_menu_btn=$("#close-menu-btn");
let active_btn = $("button[dt-active='true']");


menu_btn.on("click",function(){
  menu_div.removeClass("hidden");
});
close_menu_btn.on("click",function(){
  menu_div.addClass("hidden")
});
// Use Delegation: Listen on the parent (dash_ul) instead of a loop
dash_ul.on("htmx:afterRequest", "button", function (e) {
  const clicked_btn = $(e.detail.elt);
  if(!active_btn.is(clicked_btn)){
     clicked_btn
       .removeAttr("hx-get")
       .addClass("btn-primary")
       .attr("dt-active", "true");

     // 2. Restore the previous active button
     const prev_btn_label = active_btn.text().trim();
     const btn_data = path_obj[prev_btn_label];

     if (btn_data) {
       const span = $("<span></span>")
         .addClass("loading loading-spinner loading-sm htmx-indicator")
         .attr("id", `${btn_data["link_id"]}-indicator`);
       active_btn
         .attr("hx-get", btn_data["link"])
         .removeClass("btn-primary")
         .removeAttr("dt-active");
       if (active_btn.children("span").length == 0) {
         active_btn.append(span);
       }
       // IMPORTANT: Tell HTMX to initialize the new hx-get attribute
       htmx.process(active_btn[0]);
     }

     // 3. Update the reference to the currently active button
     active_btn = clicked_btn;
  }
});
