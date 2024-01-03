from avlwrapper import Configuration
import avlwrapper as avl
import json
from math import radians, sqrt, tan
from dataclasses import dataclass, field


@dataclass
class WingSection:
    span_tip: float
    sweep: float
    chord_tip: float
    airfoil: avl.model.Airfoil
    init_point: avl.Point
    init_chord: float

    def get_wing_tip_offset(self):
        return avl.Point(x = self.init_point.x + (self.span_tip*tan(self.sweep)),
                         y = self.init_point.y + self.span_tip,
                         z = 0)
    
    def get_area(self):
        return (self.init_chord+self.chord_tip)*self.span_tip/2
    
    def get_avl_section(self):
        return avl.Section(leading_edge_point=self.get_wing_tip_offset(),
                                    chord=self.chord_tip,
                                    airfoil=self.airfoil)



my_config = Configuration('D:\\gitd\\duneglider\\duneglider\\f_utils\\avl_config.cfg')

#       --------- 
# -------  root  -------
# -    -
# tip  sec1
wing_max_span = 3   
wing_ref_chord = 1
wing_sweep = radians(40)

wing_root_pnt = avl.Point(0, 0, 0)

wing_sec1_pct = 0.2

wing_sec1 = WingSection( span_tip=(wing_sec1_pct*wing_max_span)/2,
                         sweep = 0,
                         chord_tip = (1+wing_sec1_pct)*wing_ref_chord,
                         airfoil = avl.NacaAirfoil('2414'),
                         init_point = wing_root_pnt,
                         init_chord = wing_ref_chord)

wing_sec2 = WingSection( span_tip=(wing_max_span-wing_sec1_pct*wing_max_span)/2,
                         sweep = wing_sweep,
                         chord_tip = wing_ref_chord,
                         airfoil = avl.NacaAirfoil('2414'),
                         init_point = wing_sec1.get_wing_tip_offset(),
                         init_chord = wing_sec1.chord_tip)


root_section = avl.Section(leading_edge_point=wing_root_pnt,
                           chord=wing_ref_chord,
                           airfoil=avl.NacaAirfoil('2414'))

section_1_wing = wing_sec1.get_avl_section()

section_2_wing = wing_sec2.get_avl_section()

wing = avl.Surface(name='wing',
                   n_chordwise=12,
                   chord_spacing=avl.Spacing.cosine,
                   n_spanwise=20,
                   span_spacing=avl.Spacing.cosine,
                   y_duplicate=0.0,
                   sections=[root_section, section_1_wing, section_2_wing])

wing_area = (wing_sec1.get_area() + wing_sec2.get_area())*2

# calculate the m.a.c. leading edge location
def mac_le_pnt(root_chord, tip_chord, root_pnt, tip_pnt):
    pnt = ((2*root_chord*root_pnt[dim] +
            root_chord*tip_pnt[dim] + 
            tip_chord*root_pnt[dim] +
            2*tip_chord*tip_pnt[dim]) / 
           (3*(root_chord+tip_chord))
           for dim in range(3))
    return avl.Point(*pnt)

mach = 0

# TODO: This is wrong
le_pnt = mac_le_pnt(wing_ref_chord, wing_sec2.chord_tip,
                    wing_root_pnt, wing_sec2.get_wing_tip_offset())

ref_pnt = avl.Point(x=le_pnt.x + 0.25*wing_ref_chord,
                    y=le_pnt.y, 
                    z=le_pnt.z)

aircraft = avl.Aircraft(name='aircraft',
                        reference_area=wing_area,
                        reference_chord=wing_ref_chord,
                        reference_span=wing_ref_chord,
                        reference_point=ref_pnt,
                        mach=mach,
                        surfaces=[wing])

# create a session with only the geometry
session = avl.Session(geometry=aircraft, config=my_config)

# check if we have ghostscript
session.show_geometry()


# create a function for showing the Trefftz plot, since we'll be using it more often
def show_treffz(session):
    if 'gs_bin' in session.config.settings:
        images = session.save_trefftz_plots()
        for img in images:
            avl.show_image(img)
    else:
        for idx, _ in enumerate(session.cases):
            session.show_trefftz_plot(idx+1) # cases start from 1


simple_case = avl.Case(name='zero_aoa',
                       alpha=50)
session = avl.Session(geometry=aircraft, cases=[simple_case], config=my_config)

show_treffz(session)

# results are in a dictionary
result = session.run_all_cases()
print("CL = {}".format(result[1]['Totals']['CLtot']))