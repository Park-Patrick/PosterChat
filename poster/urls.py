from django.urls import path, include
from .views import (
	PostListView,
	PostListView00,
	PostListView1,
	PostListView2,
	PostListView3,
	PostListView4,
	PostListView5,
	PostListView6,
	PostListView7,
	PostListView8,
	PostListView9,
	PostListView10,
	PostListView11,
	PostListView12,
	PostListView13,
	PostListView14,
	PostListView15,
	PostListView16,
	PostListView17,
	PostListView18,
	PostListView19,
	PostListView20,
	PostListView21,
	PostListView22,
	PostListView23,
	PostListView24,
	PostListView25,
	PostListView26,
	PostListView27,
	PostListView28,
	PostListView29,
	PostListView30,
	PostListView31,
	PostListView32,
	PostListView33,
	PostListView34,
	PostListView35,
	PostListView36,
	PostListView37,
	PostListView38,
	PostListView39,
	PostListView40,
	PostListView41,
	PostListView42,
	PostListView43,
	PostListView44,
	PostListView45,
	PostListView46,
	PostListView47,
	PostListView48,
	PostListView49,
	PostListView50,
	PostListView51,
	PostListViewA,
	PostListViewB,
	PostListViewC,
	PostListViewD,
	PostListViewE,
	PostListViewF,
	PostListViewG,
	PostListViewH,
	PostListViewart1,
	PostListViewart2,
	PostListViewart3,
	PostListViewart4,
	PostListViewart5,
	PostListViewart6
)

app_name = 'poster'

urlpatterns = [
#local : http://127.0.0.1:8000/
	path('', PostListView.as_view(), name='post_list'),
	path('00/', PostListView1.as_view(), name='post_list00'),
	path('1/', PostListView1.as_view(), name='post_list1'),
	path('2/', PostListView2.as_view(), name='post_list2'),
	path('3/', PostListView3.as_view(), name='post_list3'),
	path('4/', PostListView4.as_view(), name='post_list4'),
	path('5/', PostListView5.as_view(), name='post_list5'),
	path('6/', PostListView6.as_view(), name='post_list6'),
	path('7/', PostListView7.as_view(), name='post_list7'),
	path('8/', PostListView8.as_view(), name='post_list8'),
	path('9/', PostListView9.as_view(), name='post_list9'),
	path('10/', PostListView10.as_view(), name='post_list10'),
	path('11/', PostListView11.as_view(), name='post_list11'),
	path('12/', PostListView12.as_view(), name='post_list12'),
	path('13/', PostListView13.as_view(), name='post_list13'),
	path('14/', PostListView14.as_view(), name='post_list14'),
	path('15/', PostListView15.as_view(), name='post_list15'),
	path('16/', PostListView16.as_view(), name='post_list16'),
	path('17/', PostListView17.as_view(), name='post_list17'),
	path('18/', PostListView18.as_view(), name='post_list18'),
	path('19/', PostListView19.as_view(), name='post_list19'),
	path('20/', PostListView20.as_view(), name='post_list20'),
	path('21/', PostListView21.as_view(), name='post_list21'),
	path('22/', PostListView22.as_view(), name='post_list22'),
	path('23/', PostListView23.as_view(), name='post_list23'),
	path('24/', PostListView24.as_view(), name='post_list24'),
	path('25/', PostListView25.as_view(), name='post_list25'),
	path('26/', PostListView26.as_view(), name='post_list26'),
	path('27/', PostListView27.as_view(), name='post_list27'),
	path('28/', PostListView28.as_view(), name='post_list28'),
	path('29/', PostListView29.as_view(), name='post_list29'),
	path('30/', PostListView30.as_view(), name='post_list30'),
	path('31/', PostListView31.as_view(), name='post_list31'),
	path('32/', PostListView32.as_view(), name='post_list32'),
	path('33/', PostListView33.as_view(), name='post_list33'),
	path('34/', PostListView34.as_view(), name='post_list34'),
	path('35/', PostListView35.as_view(), name='post_list35'),
	path('36/', PostListView36.as_view(), name='post_list36'),
	path('37/', PostListView37.as_view(), name='post_list37'),
	path('38/', PostListView38.as_view(), name='post_list38'),
	path('39/', PostListView39.as_view(), name='post_list39'),
	path('40/', PostListView40.as_view(), name='post_list40'),
	path('41/', PostListView41.as_view(), name='post_list41'),
	path('42/', PostListView42.as_view(), name='post_list42'),
	path('43/', PostListView43.as_view(), name='post_list43'),
	path('44/', PostListView44.as_view(), name='post_list44'),
	path('45/', PostListView45.as_view(), name='post_list45'),
	path('46/', PostListView46.as_view(), name='post_list46'),
	path('47/', PostListView47.as_view(), name='post_list47'),
	path('48/', PostListView48.as_view(), name='post_list48'),
	path('49/', PostListView49.as_view(), name='post_list49'),
	path('50/', PostListView50.as_view(), name='post_list50'),
	path('51/', PostListView51.as_view(), name='post_list51'),
	path('a/', PostListViewA.as_view(), name='post_lista'),
	path('b/', PostListViewB.as_view(), name='post_listb'),
	path('c/', PostListViewC.as_view(), name='post_listc'),
	path('d/', PostListViewD.as_view(), name='post_listd'),
	path('e/', PostListViewE.as_view(), name='post_liste'),
	path('f/', PostListViewF.as_view(), name='post_listf'),
	path('g/', PostListViewG.as_view(), name='post_listg'),
	path('h/', PostListViewH.as_view(), name='post_listh'),
	path('art1/', PostListViewart1.as_view(), name='post_listart1'),
	path('art2/', PostListViewart2.as_view(), name='post_listart2'),
	path('art3/', PostListViewart3.as_view(), name='post_listart3'),
	path('art4/', PostListViewart4.as_view(), name='post_listart4'),
	path('art5/', PostListViewart5.as_view(), name='post_listart5'),
	path('art6/', PostListViewart6.as_view(), name='post_listart6')
]