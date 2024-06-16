from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from data import restaurants, details
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class RestaurantList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(restaurants),
            "restaurants": restaurants
        }

class RestaurantDetail(Resource):
    def get(self, restaurant_id):
        if restaurant_id in details:
            return {
                "error": False,
                "message": "success",
                "restaurant": details[restaurant_id]
            }
        return {"error": True, "message": "Restaurant not found"}, 404

class RestaurantSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [r for r in restaurants if query in r['name'].lower() or query in r['description'].lower()]
        return {
            "error": False,
            "founded": len(result),
            "restaurants": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        restaurant_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if restaurant_id in details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            details[restaurant_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "customerReviews": details[restaurant_id]['customerReviews']
            }
        return {"error": True, "message": "Restaurant not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        restaurant_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if restaurant_id in details:
            reviews = details[restaurant_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Restaurant not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        restaurant_id = data.get('id')
        name = data.get('name')
        
        if restaurant_id in details:
            reviews = details[restaurant_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Restaurant not found"}, 404

api.add_resource(RestaurantList, '/list')
api.add_resource(RestaurantDetail, '/detail/<string:restaurant_id>')
api.add_resource(RestaurantSearch, '/search')
api.add_resource(AddReview, '/review')
api.add_resource(UpdateReview, '/review/update')
api.add_resource(DeleteReview, '/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
