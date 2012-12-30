from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
from renderpdf import render_to_pdf
from takestock.models import Stock, StockInstance, Member, Club
from datetime import date

def index(request):
    return render_to_response('takestock/index.html', {}, context_instance=RequestContext(request))

def club_general(request):
    club_list = get_list_or_404(Club)
    return render_to_response('takestock/club_general.html',{'club_list': club_list}, context_instance=RequestContext(request))

def club_detail(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    return render_to_response('takestock/club_detail.html',{'club': club}, context_instance=RequestContext(request))

def club_detail_pdf(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    response = render_to_pdf(
        'takestock/club_detail_pdf.html',
        {
            'club':club,
        }
    )
    #response['Content-Disposition'] = 'attachment; filename="{filename}.pdf"'.format(filename=str(club)+" - "+str(date.today()))
    return response
    
