const products = JSON.parse($("#products").text());
const parent_div = $("#cart-products");
const complete_sale = $("#complete-sale");
const complete_sale_btn = $("#complete-sale-btn");
const error_msg = $("#error-msg");
const dialog_s = $("#complete_sale_dialog");
const amount_card = $("#amount-card");
const payment_mcard = $("#payment-methods");
const product_data_form = $("#product-data-form");
let default_payment_method = payment_mcard.find("input[checked='checked']");

// Refactored submit_data to use an array for products
const submit_data = {
  total_price: 0,
  products: [],
};

// Initialize the cart
products.forEach((elem) => {
  createCartItems(elem, parent_div);
});

// Open Dialog and Validate
complete_sale.on("click", function () {
  // Check the products array for any null or empty IMEIs
  const has_null_imei = submit_data.products.some((item) => {
    if (item.imei_data) {
      return Object.values(item.imei_data).some(
        (val) => val === null || val.trim() === "",
      );
    }
    return false;
  });

  if (has_null_imei) {
    error_msg.html(
      "To complete sale, all phone products should have their <b>IMEI</b> values set.",
    );
  } else {
    error_msg.html("");
    dialog_s[0].showModal();
    setAmount(default_payment_method, amount_card, submit_data["total_price"]);

    const payment_methods = payment_mcard.find("input[type='radio']");
    $.each(payment_methods, function (_, elem) {
      const radio = $(elem);
      radio.on("change", function () {
        amount_card.html("");
        setAmount($(this), amount_card, submit_data["total_price"]);
      });
    });
  }
});

// Prepare data for form submission
complete_sale_btn.on("click", function (e) {
  const products_data = $("input[name='products-data']");
  // Stringify the structured submit_data (including the products list)
  products_data.val(JSON.stringify(submit_data));
});

function createCartItems(product, parent) {
  const prod_pk = product["product_pk"];
  const class_name=product["class_name"];
  const product_name = product["product_name"];
  const product_price = product["product_sell_price"];
  const product_tprice = product_price * product["count"];
  let discount_applied = false;

  // 1. Create a reference object for this specific product
  const product_entry = {
    product_pk: prod_pk,
    total_price: product_tprice,
    count: product["count"],
    class_name:class_name
  };

  // 2. Add to global submit_data
  submit_data.products.push(product_entry);
  submit_data["total_price"] += product_tprice;

  // UI Construction
  const main_div = $("<div></div>").addClass(
    "flex flex-col gap-2 p-2 border rounded-md",
  );
  const fn_div = $("<div></div>").addClass(
    "flex flex-col justify-center md:flex-row md:justify-between",
  );
  const div_1 = $("<div></div>").addClass(
    "flex justify-between items-center p-2 w-full md:w-2/3",
  );
  const div_2 = $("<div></div>").addClass(
    "flex justify-end items-center w-full p-2 gap-2 w-full md:w-1/3",
  );

  const name_elem = $("<h2></h2>").addClass("font-bold").text(product_name);
  const price_elem = $("<span></span>").text(
    `@$ ${product_price.toLocaleString()}`,
  );
  const tprice_elem = $("<span></span>")
    .html(`<b>Total:</b> $ ${product_tprice.toLocaleString()}`)
    .addClass("font-bold text-md");

  const discount_btn = $("<button></button>")
    .addClass("btn btn-sm btn-primary")
    .text("Apply Discount");
  const delete_btn = $("<button></button>")
    .addClass("btn btn-sm btn-error")
    .attr(product["delete_info"])
    .html(
      '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/><path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/></svg>',
    );

  const delete_indicator = $("<span></span>")
    .addClass("loading loading-sm loading-spinner htmx-indicator")
    .attr({ id: `delete-${product["product_pk"]}-indicator` });
  delete_btn.append(delete_indicator);

  // Discount Logic
  discount_btn.on("click", function () {
    let new_total;
    const discount_val = product["discount"] * product["count"];

    if (!discount_applied) {
      new_total = product_tprice - discount_val;
      discount_applied = true;
      $(this)
        .removeClass("btn-primary")
        .addClass("btn-secondary")
        .text("Reverse Discount");
      submit_data["total_price"] -= discount_val;
    } else {
      new_total = product_tprice;
      discount_applied = false;
      $(this)
        .removeClass("btn-secondary")
        .addClass("btn-primary")
        .text("Apply Discount");
      submit_data["total_price"] += discount_val;
    }

    // Update both the UI and the object reference in our array
    tprice_elem.html(`<b>Total:</b> $ ${new_total.toLocaleString()}`);
    product_entry.total_price = new_total;
  });

  div_1.append(name_elem, price_elem, tprice_elem);
  div_2.append(discount_btn, delete_btn);
  fn_div.append(div_1, div_2);
  main_div.append(fn_div);

  // IMEI Logic
  if (Object.keys(product).includes("sim_count")) {
    product_entry["imei_data"] = {};
    const imei_div = $("<div></div>").addClass(
      "flex flex-col md:flex-row md:justify-between md:items-center gap-2",
    );
    const h2 = $("<h2></h2>").text("Phone IMEIs").addClass("font-bold");
    imei_div.append(h2);

    product["sim_count"].forEach((elem) => {
      product_entry["imei_data"][`imei-${elem}`] = null;

      const fieldset = $("<fieldset></fieldset>").addClass("fieldset w-full");
      const legend = $("<legend></legend>")
        .addClass("fieldset-legend")
        .text(`IMEI ${elem}`);
      const input = $("<input></input>")
        .addClass("input input-sm w-full")
        .attr({ name: `imei${elem}` })
        .prop("required", true);

      input.on("change", function () {
        // Directly updates the object inside the products array
        product_entry["imei_data"][`imei-${elem}`] = $(this).val();
      });

      fieldset.append(legend, input);
      imei_div.append(fieldset);
    });
    main_div.append(imei_div);
  }

  parent.append(main_div);
}

function setAmount(payment_mtype, _amount_card, t_amount) {
  const fieldset = $("<fieldset></fieldset>").addClass("fieldset");
  const legend = $("<legend></legend>")
    .addClass("fieldset-legend")
    .text("Cash Amount");
  
  const input_elem = $("<input/>")
    .addClass("input input-sm w-full cursor-not-allowed")
    .attr({ name: "cash-amount", type: "number" })
    .prop({ readonly: true, required: true })
    .val(t_amount);

  fieldset.append(legend, input_elem);
  _amount_card.append(fieldset);
}
