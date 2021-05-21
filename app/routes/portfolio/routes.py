from flask import render_template, request, url_for, flash, redirect
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import db, Portfolio, User, Transaction_types, Transaction, app, add_transaction
from app.domain_logic.utils import return_error
from app.routes.portfolio import bp
from app.routes.portfolio.forms import AddTransactionForm


def view_user_dlc(*args, **kwargs):
    portfolio_id = request.view_args['portfolio_id']
    portfolio = db.session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    return [{'text': portfolio.title, 'url': url_for('portfolio.portfolio', portfolio_id=portfolio_id)}]


@bp.route('/<int:portfolio_id>/', methods=['GET', 'POST'])
@register_breadcrumb(bp, '.portfolio', '', dynamic_list_constructor=view_user_dlc)
@login_required
def portfolio(portfolio_id):
    USER_ID = current_user.get_id()
    portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id, user_id=USER_ID).first()
    user = db.session.query(User).filter_by(id=USER_ID).first()

    if portfolio is None:
        return return_error(500, 'Not allowed!')

    add_transaction_form = AddTransactionForm()
    add_transaction_form.portfolio.choices = [(pf.id, pf.title) for pf in
                                              db.session.query(Portfolio).filter_by(user_id=USER_ID).all()]

    if add_transaction_form.validate_on_submit():  # todo check if portfolio is owned by user

        data = {'portfolio': int(add_transaction_form.portfolio.data), 'symbol': add_transaction_form.symbol.data,
                'date': add_transaction_form.date.data.strftime('%d.%m.%y'),
                'transaction_type': int(add_transaction_form.transaction_type.data),
                'price': add_transaction_form.price.data, 'quantity': add_transaction_form.quantity.data,
                'fee': add_transaction_form.fee.data}

        if data['transaction_type'] == 4:
            data['symbol'] = None

        print(data)

        add_transaction(data['portfolio'], data['symbol'], data['date'], data['transaction_type'], data['price'],
                        data['quantity'], data['fee'])

        flash("Successfully added Transaction to Portfolio '{}'".format(portfolio.title))

        flash(
            "add_transaction(pf_id={}, symbol='{}', transcation_type={}, quantity={}, price={}, timestamp='{}', cost={})".format(
                data['portfolio'],
                data['symbol'],
                data['transaction_type'],
                data['quantity'],
                data['price'],
                data['date'],
                data['fee']))

        app.logger.info("Successfully added to Portfolio '{}'".format(portfolio.title))
        return redirect(url_for('portfolio.portfolio', portfolio_id=portfolio_id))

    symbols = [s.symbol for s in portfolio.positions]

    templateData = {
        'user': user,
        'portfolio': portfolio,
        'assets': portfolio.positions,
        'symbols': symbols,
        'symbol_list': ','.join(symbols),
        'add_transaction_form': add_transaction_form,
        'transaction_types': db.session.query(Transaction_types).order_by(Transaction_types.sort).all(),
    }

    return render_template('portfolio/portfolio_base.html', **templateData, title=(portfolio.title))
