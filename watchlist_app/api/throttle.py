from rest_framework.throttling import UserRateThrottle

class ReviewsCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    
class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list' 
