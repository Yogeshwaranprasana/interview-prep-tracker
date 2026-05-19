from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from applications.models import Application


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = '/login/'
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        search_query = request.GET.get('search', '').strip()
        status_filter = request.GET.get('status', '').strip()

        base_applications = Application.objects.filter(user=request.user)
        applications = base_applications.order_by('-created_at')

        if search_query:
            applications = applications.filter(
                company_name__icontains=search_query
            ) | applications.filter(
                job_role__icontains=search_query
            )
            applications = applications.distinct()

        if status_filter in ['Pending', 'Selected', 'Rejected']:
            applications = applications.filter(status=status_filter)

        context.update({
            'applications': applications,
            'total_applications': base_applications.count(),
            'selected_count': base_applications.filter(status='Selected').count(),
            'pending_count': base_applications.filter(status='Pending').count(),
            'rejected_count': base_applications.filter(status='Rejected').count(),
            'recent_applications': base_applications.order_by('-created_at')[:5],
            'search_query': search_query,
            'status_filter': status_filter,
        })
        return context
