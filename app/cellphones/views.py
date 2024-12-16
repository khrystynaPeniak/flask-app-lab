from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from . import cellphone_bp
from .forms import CellphoneForm, SearchFilterForm
from .models import Cellphone, CellphoneCategory
from sqlalchemy import asc, desc
from app import db

@cellphone_bp.route('/')
def get_cellphones():
    form = SearchFilterForm()
    form.all_categories()
    

    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')
    category_id = request.args.get('category', type=int)

    query = Cellphone.query

    if search_query:
        query = query.filter(Cellphone.name.ilike(f'%{search_query}%'))

    if category_id and category_id != 0:
        query = query.filter(Cellphone.category_id == category_id)

    if sort_by == 'name':
        sort_column = Cellphone.name
    elif sort_by == 'price':
        sort_column = Cellphone.price
    elif sort_by == 'category':
        sort_column = CellphoneCategory.category_name
        query = query.join(CellphoneCategory)
    else:
        sort_column = Cellphone.name

    if sort_order == 'desc':
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    cellphones = query.all()
    
    form.search.data = search_query
    form.sort_by.data = sort_by
    form.sort_order.data = sort_order
    if category_id:
        form.category.data = category_id

    return render_template('cellphones.html',
                         cellphones=cellphones,
                         form=form)

    
@cellphone_bp.route('/create-cellphone', methods=['GET', 'POST'])
@login_required
def create_cellphone():
    form = CellphoneForm()
    form.all_categories()
    
    
    if form.validate_on_submit():
        cellphone = Cellphone(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(cellphone)
        db.session.commit()
        flash('Cellphone added successfully!', 'success')
        return redirect(url_for('.get_cellphones'))
    
    return render_template('add_cellphone.html', form=form)

@cellphone_bp.route('/<int:id>')
def detail_cellphone(id):
    cellphone = Cellphone.query.get_or_404(id)
    return render_template('detail_cellphone.html', cellphone=cellphone)

@cellphone_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_cellphone(id):
    cellphone = Cellphone.query.get_or_404(id)
    
    if cellphone.user_id != current_user.id:
        abort(403)
    
    form = CellphoneForm()
    form.all_categories()
    
    
    if form.validate_on_submit():
        cellphone.name = form.name.data
        cellphone.description = form.description.data
        cellphone.price = form.price.data
        cellphone.category_id = form.category.data
        db.session.commit()
        flash('Cellphone updated successfully!', 'success')
        return redirect(url_for('.detail_cellphone', id=cellphone.id))
    
    elif request.method == 'GET':
        form.name.data = cellphone.name
        form.description.data = cellphone.description
        form.price.data = cellphone.price
        form.category.data = cellphone.category_id
    
    return render_template('edit_cellphone.html', form=form, cellphone=cellphone)

@cellphone_bp.route('/<int:id>/delete-cellphone', methods=['POST'])
@login_required
def delete_cellphone(id):
    cellphone = Cellphone.query.get_or_404(id)
    
    if cellphone.user_id != current_user.id:
        abort(403)
    
    db.session.delete(cellphone)
    db.session.commit()
    flash('Cellphone deleted successfully!', 'success')
    return redirect(url_for('.get_cellphones'))