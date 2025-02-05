#include <cxxrtl/cxxrtl.h>

#if defined(CXXRTL_INCLUDE_CAPI_IMPL) || \
    defined(CXXRTL_INCLUDE_VCD_CAPI_IMPL)
#include <cxxrtl/capi/cxxrtl_capi.cc>
#endif

#if defined(CXXRTL_INCLUDE_VCD_CAPI_IMPL)
#include <cxxrtl/capi/cxxrtl_capi_vcd.cc>
#endif

using namespace cxxrtl_yosys;

namespace cxxrtl_design {

// \keep: 1
// \top: 1
// \src: /home/lila/git/amaranth-exercises/lila/02.py:86
// \generator: Amaranth
struct p_top : public module {
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:29
	/*output*/ value<1> p_invalid;
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:28
	/*output*/ value<14> p_next__year;
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:27
	/*output*/ value<4> p_next__month;
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:26
	/*output*/ value<5> p_next__day;
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:23
	/*input*/ value<14> p_year;
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:22
	/*input*/ value<4> p_month;
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:21
	/*input*/ value<5> p_day;
	// \hdlname: next_day$7 leap_year
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:32
	/*outline*/ value<1> p_next__day_24_7_2e_leap__year;
	// \hdlname: next_day$7 day_in_month
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:33
	/*outline*/ value<5> p_next__day_24_7_2e_day__in__month;
	// \hdlname: next_day$7 invalid
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:29
	/*outline*/ value<1> p_next__day_24_7_2e_invalid;
	// \hdlname: next_day$7 next_day
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:26
	/*outline*/ value<5> p_next__day_24_7_2e_next__day;
	// \hdlname: next_day$7 next_month
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:27
	/*outline*/ value<4> p_next__day_24_7_2e_next__month;
	// \hdlname: next_day$7 next_year
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:28
	/*outline*/ value<14> p_next__day_24_7_2e_next__year;
	value<2> cell_i_84;
	value<2> cell_i_79;
	value<2> cell_i_71;
	value<2> cell_i_65;
	value<2> cell_i_60;
	value<2> cell_i_47;
	p_top(interior) {}
	p_top() {
		reset();
	};

	void reset() override;

	bool eval(performer *performer = nullptr) override;

	template<class ObserverT>
	bool commit(ObserverT &observer) {
		bool changed = false;
		return changed;
	}

	bool commit() override {
		observer observer;
		return commit<>(observer);
	}

	void debug_eval();
	debug_outline debug_eval_outline { std::bind(&p_top::debug_eval, this) };

	void debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs = {}) override;
}; // struct p_top

void p_top::reset() {
	cell_i_84 = {};
	cell_i_79 = {};
	cell_i_71 = {};
	cell_i_65 = {};
	cell_i_60 = {};
	cell_i_47 = {};
}

bool p_top::eval(performer *performer) {
	bool converged = true;
	value<7> i_procmux_24_6__CMP;
	value<4> i_procmux_24_5__CMP;
	// \hdlname: next_day$7 day_in_month
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:33
	value<5> p_next__day_24_7_2e_day__in__month;
	// \hdlname: next_day$7 day
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:21
	value<5> p_next__day_24_7_2e_day;
	// \hdlname: next_day$7 month
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:22
	value<4> p_next__day_24_7_2e_month;
	// \hdlname: next_day$7 year
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:23
	value<14> p_next__day_24_7_2e_year;
	// \hdlname: next_day$7 invalid
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:29
	value<1> p_next__day_24_7_2e_invalid;
	value<1> i_flatten_5c_next__day_24_7_2e__24_17;
	value<14> i_32;
	// connection
	p_next__day_24_7_2e_year = p_year;
	// connection
	p_next__day_24_7_2e_month = p_month;
	// \full_case: 1
	// cell $procmux$5_CMP0
	i_procmux_24_5__CMP.slice<0>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x4u});
	// \full_case: 1
	// cell $procmux$5_CMP1
	i_procmux_24_5__CMP.slice<1>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x6u});
	// \full_case: 1
	// cell $procmux$5_CMP2
	i_procmux_24_5__CMP.slice<2>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x9u});
	// \full_case: 1
	// cell $procmux$5_CMP3
	i_procmux_24_5__CMP.slice<3>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0xbu});
	// \full_case: 1
	// cell $procmux$6_CMP0
	i_procmux_24_6__CMP.slice<0>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x1u});
	// \full_case: 1
	// cell $procmux$6_CMP1
	i_procmux_24_6__CMP.slice<1>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x3u});
	// \full_case: 1
	// cell $procmux$6_CMP2
	i_procmux_24_6__CMP.slice<2>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x5u});
	// \full_case: 1
	// cell $procmux$6_CMP3
	i_procmux_24_6__CMP.slice<3>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x7u});
	// \full_case: 1
	// cell $procmux$6_CMP4
	i_procmux_24_6__CMP.slice<4>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x8u});
	// \full_case: 1
	// cell $procmux$6_CMP5
	i_procmux_24_6__CMP.slice<5>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0xau});
	// \full_case: 1
	// cell $procmux$6_CMP6
	i_procmux_24_6__CMP.slice<6>() = eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0xcu});
	// cells $procmux$3 $procmux$4_CMP0 $procmux$5_ANY $procmux$6_ANY $flatten\next_day$7.$38 $flatten\next_day$7.$37 $flatten\next_day$7.$36 $flatten\next_day$7.$32 $flatten\next_day$7.$30 $flatten\next_day$7.$26
	p_next__day_24_7_2e_day__in__month = (eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0x2u}) ? (and_uu<1>(logic_not<1>(modfloor_uu<14>(p_next__day_24_7_2e_year, value<3>{0x4u}).slice<2,0>().val()), reduce_bool<1>(modfloor_uu<14>(p_next__day_24_7_2e_year, value<7>{0x64u}).slice<6,0>().val())) ? value<5>{0x1du} : value<5>{0x1cu}) : (reduce_or<1>(i_procmux_24_5__CMP) ? value<5>{0x1eu} : (reduce_or<1>(i_procmux_24_6__CMP) ? value<5>{0x1fu} : value<5>{0u})));
	// connection
	p_next__day_24_7_2e_day = p_day;
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:68
	// cell $flatten\next_day$7.$51
	i_flatten_5c_next__day_24_7_2e__24_17 = eq_uu<1>(p_next__day_24_7_2e_day, p_next__day_24_7_2e_day__in__month);
	// cells $flatten\next_day$7.$49 $flatten\next_day$7.$48 $flatten\next_day$7.$47 $flatten\next_day$7.$46 $flatten\next_day$7.$45 $flatten\next_day$7.$44 $flatten\next_day$7.$43 $flatten\next_day$7.$42 $flatten\next_day$7.$41 $flatten\next_day$7.$40 $flatten\next_day$7.$39
	p_next__day_24_7_2e_invalid = or_uu<1>(or_uu<1>(or_uu<1>(or_uu<1>(or_uu<1>(logic_not<1>(p_next__day_24_7_2e_day), gt_uu<1>(p_next__day_24_7_2e_day, p_next__day_24_7_2e_day__in__month)), logic_not<1>(p_next__day_24_7_2e_month)), gt_uu<1>(p_next__day_24_7_2e_month, value<4>{0xcu})), logic_not<1>(p_next__day_24_7_2e_year)), gt_uu<1>(p_next__day_24_7_2e_year, value<14>{0x270fu}));
	// connection
	i_32.slice<0>() = p_year.slice<0>().val();
	// connection
	i_32.slice<13,1>() = value<13>{0u};
	// cells $procmux$20 $procmux$18 $flatten\next_day$7.$57 $flatten\next_day$7.$56 $flatten\next_day$7.$55
	p_next__year = (p_next__day_24_7_2e_invalid ? value<14>{0u} : (i_flatten_5c_next__day_24_7_2e__24_17 ? (eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0xcu}) ? add_uu<15>(p_next__day_24_7_2e_year, value<1>{0x1u}) : value<1>{0u}.concat(p_next__day_24_7_2e_year).val()).slice<13,0>().val() : p_year));
	// cells $procmux$15 $procmux$13 $flatten\next_day$7.$54 $flatten\next_day$7.$53 $flatten\next_day$7.$52
	p_next__month = (p_next__day_24_7_2e_invalid ? value<4>{0u} : (i_flatten_5c_next__day_24_7_2e__24_17 ? (eq_uu<1>(p_next__day_24_7_2e_month, value<4>{0xcu}) ? value<5>{0x1u} : add_uu<5>(p_next__day_24_7_2e_month, value<1>{0x1u})).slice<3,0>().val() : p_month));
	// cells $procmux$10 $procmux$8 $flatten\next_day$7.$58
	p_next__day = (p_next__day_24_7_2e_invalid ? value<5>{0u} : (i_flatten_5c_next__day_24_7_2e__24_17 ? value<5>{0x1u} : add_uu<6>(p_next__day_24_7_2e_day, value<1>{0x1u}).slice<4,0>().val()));
	// connection
	p_invalid = p_next__day_24_7_2e_invalid;
	// cells $47 $45 $44 $43 $42 $41 $40
	auto cell_i_47_next = value<1>{0x1u}.concat(eq_uu<1>(p_invalid, or_uu<1>(or_uu<1>(logic_not<1>(p_next__year), logic_not<1>(p_next__month)), logic_not<1>(p_next__day)))).val();
	if (cell_i_47 != cell_i_47_next) {
		if (value<1>{0x1u}) {
			struct : public lazy_fmt {
				std::string operator() () const override {
					std::string buf;
					return buf;
				}
				struct performer *performer;
			} formatter;
			formatter.performer = performer;
			bool condition = (bool)eq_uu<1>(p_invalid, or_uu<1>(or_uu<1>(logic_not<1>(p_next__year), logic_not<1>(p_next__month)), logic_not<1>(p_next__day)));
			if (performer) {
				static const metadata_map attributes = metadata_map({
					{ "src", "/home/lila/git/amaranth-exercises/lila/02.py:92" },
				});
				performer->on_check(flavor::ASSERT, condition, formatter, attributes);
			} else {
				if (!condition) {
					std::cerr << formatter();
				}
				CXXRTL_ASSERT(condition && "Check failed");
			}
		}
		cell_i_47 = cell_i_47_next;
	}
	// cells $60 $58 $57 $56 $55 $54 $53 $52 $51 $50 $49 $48
	auto cell_i_60_next = value<1>{0x1u}.concat(or_uu<1>(or_uu<1>(or_uu<1>(logic_not<1>(p_next__year), logic_not<1>(p_next__month)), logic_not<1>(p_next__day)), and_uu<1>(and_uu<1>(reduce_bool<1>(p_next__year), reduce_bool<1>(p_next__month)), reduce_bool<1>(p_next__day)))).val();
	if (cell_i_60 != cell_i_60_next) {
		if (value<1>{0x1u}) {
			struct : public lazy_fmt {
				std::string operator() () const override {
					std::string buf;
					return buf;
				}
				struct performer *performer;
			} formatter;
			formatter.performer = performer;
			bool condition = (bool)or_uu<1>(or_uu<1>(or_uu<1>(logic_not<1>(p_next__year), logic_not<1>(p_next__month)), logic_not<1>(p_next__day)), and_uu<1>(and_uu<1>(reduce_bool<1>(p_next__year), reduce_bool<1>(p_next__month)), reduce_bool<1>(p_next__day)));
			if (performer) {
				static const metadata_map attributes = metadata_map({
					{ "src", "/home/lila/git/amaranth-exercises/lila/02.py:95" },
				});
				performer->on_check(flavor::ASSERT, condition, formatter, attributes);
			} else {
				if (!condition) {
					std::cerr << formatter();
				}
				CXXRTL_ASSERT(condition && "Check failed");
			}
		}
		cell_i_60 = cell_i_60_next;
	}
	// cells $65 $63 $procmux$30 $procmux$28 $62
	auto cell_i_65_next = (p_next__day_24_7_2e_invalid ? value<1>{0u} : (eq_uu<1>(p_day, value<5>{0x1fu}) ? value<1>{0x1u} : value<1>{0u})).concat(eq_uu<1>(p_next__day, value<1>{0x1u})).val();
	if (cell_i_65 != cell_i_65_next) {
		if ((p_next__day_24_7_2e_invalid ? value<1>{0u} : (eq_uu<1>(p_day, value<5>{0x1fu}) ? value<1>{0x1u} : value<1>{0u}))) {
			struct : public lazy_fmt {
				std::string operator() () const override {
					std::string buf;
					return buf;
				}
				struct performer *performer;
			} formatter;
			formatter.performer = performer;
			bool condition = (bool)eq_uu<1>(p_next__day, value<1>{0x1u});
			if (performer) {
				static const metadata_map attributes = metadata_map({
					{ "src", "/home/lila/git/amaranth-exercises/lila/02.py:101" },
				});
				performer->on_check(flavor::ASSERT, condition, formatter, attributes);
			} else {
				if (!condition) {
					std::cerr << formatter();
				}
				CXXRTL_ASSERT(condition && "Check failed");
			}
		}
		cell_i_65 = cell_i_65_next;
	}
	// cells $71 $69 $procmux$26 $procmux$24 $68 $67 $66
	auto cell_i_71_next = (p_next__day_24_7_2e_invalid ? value<1>{0u} : (and_uu<1>(eq_uu<1>(p_day, value<5>{0x1fu}), eq_uu<1>(p_month, value<4>{0xcu})) ? value<1>{0x1u} : value<1>{0u})).concat(eq_uu<1>(p_next__month, value<1>{0x1u})).val();
	if (cell_i_71 != cell_i_71_next) {
		if ((p_next__day_24_7_2e_invalid ? value<1>{0u} : (and_uu<1>(eq_uu<1>(p_day, value<5>{0x1fu}), eq_uu<1>(p_month, value<4>{0xcu})) ? value<1>{0x1u} : value<1>{0u}))) {
			struct : public lazy_fmt {
				std::string operator() () const override {
					std::string buf;
					return buf;
				}
				struct performer *performer;
			} formatter;
			formatter.performer = performer;
			bool condition = (bool)eq_uu<1>(p_next__month, value<1>{0x1u});
			if (performer) {
				static const metadata_map attributes = metadata_map({
					{ "src", "/home/lila/git/amaranth-exercises/lila/02.py:105" },
				});
				performer->on_check(flavor::ASSERT, condition, formatter, attributes);
			} else {
				if (!condition) {
					std::cerr << formatter();
				}
				CXXRTL_ASSERT(condition && "Check failed");
			}
		}
		cell_i_71 = cell_i_71_next;
	}
	// cells $79 $procmux$22 $77 $76 $74 $73 $72
	auto cell_i_79_next = (reduce_bool<1>(and_uu<14>(value<13>{0u}.concat(and_uu<1>(eq_uu<1>(p_day, value<5>{0x1du}), eq_uu<1>(p_month, value<2>{0x2u}))).val(), i_32)) ? value<1>{0x1u} : value<1>{0u}).concat(p_invalid).val();
	if (cell_i_79 != cell_i_79_next) {
		if ((reduce_bool<1>(and_uu<14>(value<13>{0u}.concat(and_uu<1>(eq_uu<1>(p_day, value<5>{0x1du}), eq_uu<1>(p_month, value<2>{0x2u}))).val(), i_32)) ? value<1>{0x1u} : value<1>{0u})) {
			struct : public lazy_fmt {
				std::string operator() () const override {
					std::string buf;
					return buf;
				}
				struct performer *performer;
			} formatter;
			formatter.performer = performer;
			bool condition = (bool)p_invalid;
			if (performer) {
				static const metadata_map attributes = metadata_map({
					{ "src", "/home/lila/git/amaranth-exercises/lila/02.py:109" },
				});
				performer->on_check(flavor::ASSERT, condition, formatter, attributes);
			} else {
				if (!condition) {
					std::cerr << formatter();
				}
				CXXRTL_ASSERT(condition && "Check failed");
			}
		}
		cell_i_79 = cell_i_79_next;
	}
	// cells $84 $82 $81 $80
	auto cell_i_84_next = value<1>{0x1u}.concat(and_uu<1>(eq_uu<1>(p_next__month, value<2>{0x2u}), eq_uu<1>(p_next__day, value<5>{0x1du}))).val();
	if (cell_i_84 != cell_i_84_next) {
		if (value<1>{0x1u}) {
			struct : public lazy_fmt {
				std::string operator() () const override {
					std::string buf;
					return buf;
				}
				struct performer *performer;
			} formatter;
			formatter.performer = performer;
			bool condition = (bool)and_uu<1>(eq_uu<1>(p_next__month, value<2>{0x2u}), eq_uu<1>(p_next__day, value<5>{0x1du}));
			if (performer) {
				static const metadata_map attributes = metadata_map({
					{ "src", "/home/lila/git/amaranth-exercises/lila/02.py:112" },
				});
				performer->on_check(flavor::COVER, condition, formatter, attributes);
			} else {
			}
		}
		cell_i_84 = cell_i_84_next;
	}
	return converged;
}

void p_top::debug_eval() {
	value<7> i_procmux_24_6__CMP;
	value<4> i_procmux_24_5__CMP;
	value<1> i_flatten_5c_next__day_24_7_2e__24_17;
	// cells $flatten\next_day$7.$37 $flatten\next_day$7.$36 $flatten\next_day$7.$32 $flatten\next_day$7.$30 $flatten\next_day$7.$26
	p_next__day_24_7_2e_leap__year = and_uu<1>(logic_not<1>(modfloor_uu<14>(p_year, value<3>{0x4u}).slice<2,0>().val()), reduce_bool<1>(modfloor_uu<14>(p_year, value<7>{0x64u}).slice<6,0>().val()));
	// \full_case: 1
	// cell $procmux$5_CMP0
	i_procmux_24_5__CMP.slice<0>() = eq_uu<1>(p_month, value<4>{0x4u});
	// \full_case: 1
	// cell $procmux$5_CMP1
	i_procmux_24_5__CMP.slice<1>() = eq_uu<1>(p_month, value<4>{0x6u});
	// \full_case: 1
	// cell $procmux$5_CMP2
	i_procmux_24_5__CMP.slice<2>() = eq_uu<1>(p_month, value<4>{0x9u});
	// \full_case: 1
	// cell $procmux$5_CMP3
	i_procmux_24_5__CMP.slice<3>() = eq_uu<1>(p_month, value<4>{0xbu});
	// \full_case: 1
	// cell $procmux$6_CMP0
	i_procmux_24_6__CMP.slice<0>() = eq_uu<1>(p_month, value<4>{0x1u});
	// \full_case: 1
	// cell $procmux$6_CMP1
	i_procmux_24_6__CMP.slice<1>() = eq_uu<1>(p_month, value<4>{0x3u});
	// \full_case: 1
	// cell $procmux$6_CMP2
	i_procmux_24_6__CMP.slice<2>() = eq_uu<1>(p_month, value<4>{0x5u});
	// \full_case: 1
	// cell $procmux$6_CMP3
	i_procmux_24_6__CMP.slice<3>() = eq_uu<1>(p_month, value<4>{0x7u});
	// \full_case: 1
	// cell $procmux$6_CMP4
	i_procmux_24_6__CMP.slice<4>() = eq_uu<1>(p_month, value<4>{0x8u});
	// \full_case: 1
	// cell $procmux$6_CMP5
	i_procmux_24_6__CMP.slice<5>() = eq_uu<1>(p_month, value<4>{0xau});
	// \full_case: 1
	// cell $procmux$6_CMP6
	i_procmux_24_6__CMP.slice<6>() = eq_uu<1>(p_month, value<4>{0xcu});
	// cells $procmux$3 $procmux$4_CMP0 $procmux$5_ANY $procmux$6_ANY $flatten\next_day$7.$38 $flatten\next_day$7.$37 $flatten\next_day$7.$36 $flatten\next_day$7.$32 $flatten\next_day$7.$30 $flatten\next_day$7.$26
	p_next__day_24_7_2e_day__in__month = (eq_uu<1>(p_month, value<4>{0x2u}) ? (p_next__day_24_7_2e_leap__year ? value<5>{0x1du} : value<5>{0x1cu}) : (reduce_or<1>(i_procmux_24_5__CMP) ? value<5>{0x1eu} : (reduce_or<1>(i_procmux_24_6__CMP) ? value<5>{0x1fu} : value<5>{0u})));
	// \src: /home/lila/git/amaranth-exercises/lila/02.py:68
	// cell $flatten\next_day$7.$51
	i_flatten_5c_next__day_24_7_2e__24_17 = eq_uu<1>(p_day, p_next__day_24_7_2e_day__in__month);
	// cells $flatten\next_day$7.$49 $flatten\next_day$7.$48 $flatten\next_day$7.$47 $flatten\next_day$7.$46 $flatten\next_day$7.$45 $flatten\next_day$7.$44 $flatten\next_day$7.$43 $flatten\next_day$7.$42 $flatten\next_day$7.$41 $flatten\next_day$7.$40 $flatten\next_day$7.$39
	p_next__day_24_7_2e_invalid = or_uu<1>(or_uu<1>(or_uu<1>(or_uu<1>(or_uu<1>(logic_not<1>(p_day), gt_uu<1>(p_day, p_next__day_24_7_2e_day__in__month)), logic_not<1>(p_month)), gt_uu<1>(p_month, value<4>{0xcu})), logic_not<1>(p_year)), gt_uu<1>(p_year, value<14>{0x270fu}));
	// cells $procmux$20 $procmux$18 $flatten\next_day$7.$57 $flatten\next_day$7.$56 $flatten\next_day$7.$55
	p_next__day_24_7_2e_next__year = (p_next__day_24_7_2e_invalid ? value<14>{0u} : (i_flatten_5c_next__day_24_7_2e__24_17 ? (eq_uu<1>(p_month, value<4>{0xcu}) ? add_uu<15>(p_year, value<1>{0x1u}) : value<1>{0u}.concat(p_year).val()).slice<13,0>().val() : p_year));
	// cells $procmux$15 $procmux$13 $flatten\next_day$7.$54 $flatten\next_day$7.$53 $flatten\next_day$7.$52
	p_next__day_24_7_2e_next__month = (p_next__day_24_7_2e_invalid ? value<4>{0u} : (i_flatten_5c_next__day_24_7_2e__24_17 ? (eq_uu<1>(p_month, value<4>{0xcu}) ? value<5>{0x1u} : add_uu<5>(p_month, value<1>{0x1u})).slice<3,0>().val() : p_month));
	// cells $procmux$10 $procmux$8 $flatten\next_day$7.$58
	p_next__day_24_7_2e_next__day = (p_next__day_24_7_2e_invalid ? value<5>{0u} : (i_flatten_5c_next__day_24_7_2e__24_17 ? value<5>{0x1u} : add_uu<6>(p_day, value<1>{0x1u}).slice<4,0>().val()));
}

CXXRTL_EXTREMELY_COLD
void p_top::debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs) {
	assert(path.empty() || path[path.size() - 1] == ' ');
	if (scopes) {
		scopes->add(path.empty() ? path : path.substr(0, path.size() - 1), "top", metadata_map({
			{ "keep", UINT64_C(1) },
			{ "top", UINT64_C(1) },
			{ "src", "/home/lila/git/amaranth-exercises/lila/02.py:86" },
			{ "generator", "Amaranth" },
		}), std::move(cell_attrs));
		scopes->add(path, "next_day$7", "top.next_day$7", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:42\000generator\000sAmaranth\000", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:87\000");
	}
	if (items) {
		items->add(path, "next_day$7 leap_year", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:32\000", debug_eval_outline, p_next__day_24_7_2e_leap__year);
		items->add(path, "next_day$7 day_in_month", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:33\000", debug_eval_outline, p_next__day_24_7_2e_day__in__month);
		items->add(path, "next_day$7 day", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:21\000", debug_alias(), p_day);
		items->add(path, "next_day$7 month", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:22\000", debug_alias(), p_month);
		items->add(path, "next_day$7 year", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:23\000", debug_alias(), p_year);
		items->add(path, "next_day$7 invalid", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:29\000", debug_eval_outline, p_next__day_24_7_2e_invalid);
		items->add(path, "next_day$7 next_day", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:26\000", debug_eval_outline, p_next__day_24_7_2e_next__day);
		items->add(path, "next_day$7 next_month", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:27\000", debug_eval_outline, p_next__day_24_7_2e_next__month);
		items->add(path, "next_day$7 next_year", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:28\000", debug_eval_outline, p_next__day_24_7_2e_next__year);
		items->add(path, "invalid", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:29\000", p_invalid, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "next_year", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:28\000", p_next__year, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "next_month", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:27\000", p_next__month, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "next_day", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:26\000", p_next__day, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "year", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:23\000", p_year, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "month", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:22\000", p_month, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "day", "src\000s/home/lila/git/amaranth-exercises/lila/02.py:21\000", p_day, 0, debug_item::INPUT|debug_item::UNDRIVEN);
	}
}

} // namespace cxxrtl_design

extern "C"
cxxrtl_toplevel cxxrtl_design_create() {
	return new _cxxrtl_toplevel { std::unique_ptr<cxxrtl_design::p_top>(new cxxrtl_design::p_top) };
}
