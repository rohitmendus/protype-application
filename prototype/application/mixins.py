from django.contrib.auth.mixins import LoginRequiredMixin
class AdminRequiredMixin(LoginRequiredMixin):
    def test_func(self):
        try:
        	return self.request.user.roles.filter(role="Admin").exists()
        except:
        	return False