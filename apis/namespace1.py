
from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse
from database import db
from database.model import TodoTasks
import logging


users_api = Namespace('TodoTasks', description='TodoTasks related operations')

insert_t = users_api.model("Insert_Task",
                           {
                             "name": fields.String(description="Name", required=True),
                             "is_done": fields.Boolean(description="true or false", required=True)

                             })

example_parameters = reqparse.RequestParser()
example_parameters.add_argument('is_done_filter', type=str, help='Done or Not Done', required=False)


@users_api.route('/')
class TodoList(Resource):

    @users_api.expect(example_parameters)
    @users_api.response(200, 'Retrieve TodoTasks successfully.')
    def get(self):
        params = example_parameters.parse_args()
        is_filter = params.get('is_done_filter')
        # pprint(is_filter)
        task_lists = []
        try:
            if is_filter == 'Done':
                all_tasks = db.session.query(TodoTasks).filter(TodoTasks.is_done == 1).all()
            elif is_filter == 'Not Done':
                all_tasks = db.session.query(TodoTasks).filter(TodoTasks.is_done == 0).all()
            else:
                all_tasks = db.session.query(TodoTasks).all()
            for t in all_tasks:
                task_lists.append({'id': t.id, 'name': t.name, 'is_done': t.is_done})
            logging.info('Retrieve all TodoTasks successfully')
            return task_lists

        except Exception as e:
            logging.info('Could not get TodoTasks')
            users_api.abort(404, e.__doc__, status="Could not find information", statusCode="404")

    @users_api.response(200, 'Delete TodoTasks successfully.')
    def delete(self):
        try:
            db.session.query(TodoTasks).delete()
            db.session.commit()
            logging.info('Delete all TodoTasks successfully.')
            return {"status": "All tasks deleted"}
        except:
            db.session.rollback()
            logging.info('Could not delete TodoTasks.')
            return 404

    @users_api.expect(insert_t)
    @users_api.response(201, 'Create TodoTasks successfully.')
    def post(self):
        try:
            data = request.json
            db.session.add(TodoTasks(name=data['name'], is_done=data['is_done']))
            db.session.commit()
            logging.info('Create a TodoTask successfully.')

            return {
                "status": "TodoTask added",
                "name": data['name'],
                "is_done": data['is_done']
            }
        except Exception as e:
            logging.info('Could not create a TodoTask.')
            users_api.abort(400, e.__doc__, status="Could not save information.", statusCode="400")


@users_api.route('/<int:task_id>')
class TodoListPara(Resource):
    @users_api.response(200, 'Retrieve data successfully.')
    def get(self, task_id):
        one_task = db.session.query(TodoTasks).filter_by(id=task_id).first()
        if one_task:
            data = {'id': one_task.id, 'name': one_task.name, 'is_done': one_task.is_done}
            logging.info('Retrieve a TodoTask successfully.')
            return data
        else:
            logging.info('Could not retrieve a TodoTask.')
            return 404

    @users_api.expect(insert_t)
    @users_api.response(201, 'Update TodoTasks successfully.')
    def put(self, task_id):
        try:
            one_task = db.session.query(TodoTasks).filter_by(id=task_id).first()
            data = request.json
            one_task.name = data['name']
            one_task.is_done = data['is_done']
            db.session.commit()
            logging.info('Update a TodoTask successfully')
            return {
                "status": "One task updated",
                "name": data['name'],
                "is_done": data['is_done']
            }
        except Exception as e:
            logging.info('Could not update TodoTasks')
            users_api.abort(400, e.__doc__, status="Could not save information", statusCode="400")

    @users_api.response(200, 'A task deleted successfully.')
    def delete(self, task_id):

        d_task = db.session.query(TodoTasks).filter_by(id=task_id).first()
        if d_task:
            # pprint(delete_task)
            db.session.delete(d_task)
            db.session.commit()
            logging.info('Delete a TodoTask successfully.')
            return {"status": "One Task deleted"}
        else:
            logging.info('Could not delete the TodoTask.')
            return 404
