odoo.define('l10n_sa_e-pos.models', function (require) {
    "use strict";

    var exports = require('point_of_sale.models');
    var OrderSuper = exports.Order;
    var rpc = require('web.rpc');

    exports.Order = exports.Order.extend({
        export_for_printing: function () {
            var result = OrderSuper.prototype.export_for_printing.call(this);
            if (this.qr_code) {
                // const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter()
                // let qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(this.qr_code, 150, 150));
                // result.qr_code = "data:image/svg+xml;base64," + window.btoa(qr_code_svg);
                result.qr_code = this.qr_code;
            }
            return result;
        },
        set_qr_code: function (qr_code) {
            this.qr_code = qr_code;
        },
        get_qr_code: function () {
            self = this;
            return rpc.query({
                model: 'pos.order',
                method: 'get_qr_code',
                args: [self.backendId],
            }).then(function (qr_code) {
                return qr_code;
            });
        },
        wait_for_push_order: function () {
            var result = OrderSuper.prototype.wait_for_push_order.apply(this, arguments);
            result = Boolean(result || this.pos.company.country.code === 'SA');
            return result;
        },
    });
    exports.PosModel = exports.PosModel.extend({
        push_and_invoice_order: function (order) {
            var self = this;
            var invoiced = new Promise(function (resolveInvoiced, rejectInvoiced) {
                if (!order.get_client()) {
                    rejectInvoiced({ code: 400, message: 'Missing Customer', data: {} });
                }
                else {
                    var order_id = self.db.add_order(order.export_as_JSON());

                    self.flush_mutex.exec(function () {
                        var done = new Promise(function (resolveDone, rejectDone) {
                            // send the order to the server
                            // we have a 30 seconds timeout on this push.
                            // FIXME: if the server takes more than 30 seconds to accept the order,
                            // the client will believe it wasn't successfully sent, and very bad
                            // things will happen as a duplicate will be sent next time
                            // so we must make sure the server detects and ignores duplicated orders

                            var transfer = self._flush_orders([self.db.get_order(order_id)], { timeout: 30000, to_invoice: true });

                            transfer.catch(function (error) {
                                rejectInvoiced(error);
                                rejectDone();
                            });

                            // on success, get the order id generated by the server
                            transfer.then(function (order_server_id) {
                                // generate the pdf and download it
                                if (order_server_id.length && order.is_to_invoice()) {
                                    self.do_action('point_of_sale.pos_invoice_report', {
                                        additional_context: {
                                            active_ids: order_server_id,
                                        }
                                    }).then(function () {
                                        resolveInvoiced(order_server_id);
                                        resolveDone();
                                    }).guardedCatch(function (error) {
                                        rejectInvoiced({ code: 401, message: 'Backend Invoice', data: { order: order } });
                                        rejectDone();
                                    });
                                } else if (order_server_id.length) {
                                    resolveInvoiced(order_server_id);
                                    resolveDone();
                                } else {
                                    // The order has been pushed separately in batch when
                                    // the connection came back.
                                    // The user has to go to the backend to print the invoice
                                    rejectInvoiced({ code: 401, message: 'Backend Invoice', data: { order: order } });
                                    rejectDone();
                                }
                            });
                            return done;
                        });
                    });
                }
            });

            return invoiced;
        },
    });
});