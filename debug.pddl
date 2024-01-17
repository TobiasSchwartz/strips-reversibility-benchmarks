
    (define (domain benchmark-2-2-31-5)
    (:requirements :strips)
    (:predicates (f0) (f1) (f2) (f3) (f4) (f5) (f6) (f7) (f8) (f9) (f10) (f11) (f12) (f13) (f14) (f15) (f16) (f17) (f18) (f19) (f20) (f21) (f22) (f23) (f24) (f25) (f26) (f27) (f28) (f29) (f30) (f31) (f32) (f33) (f34) (f35) (f36) (f37) (f38) (f39) (f40) (f41) (f42) (f43) (f44) (f45) (f46) (f47) (f48) (f49) (f50) (f51) (f52) (f53) (f54) (f55) (f56) (f57) (f58) (f59) (f60) (f61) (f62) (f63) (f64) (f65) (f66) (f67) (f68) (f69) (f70) (f71) (f72) (f73) (f74) (f75) (f76) (f77) (f78) (f79) (f80) (f81) (f82) (f83) (f84) (f85) (f86) (f87) (f88) (f89) (f90) (f91) (f92) (f93) (f94) (f95) (f96) (f97) (f98) (f99) (f100) (f101) (f102) (f103) (f104) (f105) (f106) (f107) (f108) (f109) (f110) (f111) (f112) (f113) (f114) (f115) (f116) (f117) (f118) (f119) (f120) (f121) (f122) (f123) (f124) (f125) (f126) (f127) (f128) (f129) (f130) (f131) (f132) (f133) (f134) (f135) (f136) (f137) (f138) (f139) (f140) (f141) (f142) (f143) (f144) (f145) (f146) (f147) (f148) (f149) (f150) (f151) (f152) (f153) (f154) (f155) (f156) (f157) (f158))

    (:action del-all
    :precondition (and (f158) (not (f0)) (not (f1)) (not (f2)) (not (f3)) (not (f4)) (not (f5)) (not (f6)) (not (f7)) (not (f8)) (not (f9)) (not (f10)) (not (f11)) (not (f12)) (not (f13)) (not (f14)) (not (f15)) (not (f16)) (not (f17)) (not (f18)) (not (f19)) (not (f20)) (not (f21)) (not (f22)) (not (f23)) (not (f24)) (not (f25)) (not (f26)) (not (f27)) (not (f28)) (not (f29)) (not (f30)) (not (f31)) (not (f32)) (not (f33)) (not (f34)) (not (f35)) (not (f36)) (not (f37)) (not (f38)) (not (f39)) (not (f40)) (not (f41)) (not (f42)) (not (f43)) (not (f44)) (not (f45)) (not (f46)) (not (f47)) (not (f48)) (not (f49)) (not (f50)) (not (f51)) (not (f52)) (not (f53)) (not (f54)) (not (f55)) (not (f56)) (not (f57)) (not (f58)) (not (f59)) (not (f60)) (not (f61)) (not (f62)) (not (f63)) (not (f64)) (not (f65)) (not (f66)) (not (f67)) (not (f68)) (not (f69)) (not (f70)) (not (f71)) (not (f72)) (not (f73)) (not (f74)) (not (f75)) (not (f76)) (not (f77)) (not (f78)) (not (f79)) (not (f80)) (not (f81)) (not (f82)) (not (f83)) (not (f84)) (not (f85)) (not (f86)) (not (f87)) (not (f88)) (not (f89)) (not (f90)) (not (f91)) (not (f92)) (not (f93)) (not (f94)) (not (f95)) (not (f96)) (not (f97)) (not (f98)) (not (f99)) (not (f100)) (not (f101)) (not (f102)) (not (f103)) (not (f104)) (not (f105)) (not (f106)) (not (f107)) (not (f108)) (not (f109)) (not (f110)) (not (f111)) (not (f112)) (not (f113)) (not (f114)) (not (f115)) (not (f116)) (not (f117)) (not (f118)) (not (f119)) (not (f120)) (not (f121)) (not (f122)) (not (f123)) (not (f124)) (not (f125)) (not (f126)) (not (f127)) (not (f128)) (not (f129)) (not (f130)) (not (f131)) (not (f132)) (not (f133)) (not (f134)) (not (f135)) (not (f136)) (not (f137)) (not (f138)) (not (f139)) (not (f140)) (not (f141)) (not (f142)) (not (f143)) (not (f144)) (not (f145)) (not (f146)) (not (f147)) (not (f148)) (not (f149)) (not (f150)) (not (f151)) (not (f152)) (not (f153)) (not (f154)) (not (f155)) (not (f156)) (not (f157)))
    :effect (and (f0) (not (f1)) (not (f2)) (not (f3)) (not (f4)) (not (f5)) (not (f6)) (not (f7)) (not (f8)) (not (f9)) (not (f10)) (not (f11)) (not (f12)) (not (f13)) (not (f14)) (not (f15)) (not (f16)) (not (f17)) (not (f18)) (not (f19)) (not (f20)) (not (f21)) (not (f22)) (not (f23)) (not (f24)) (not (f25)) (not (f26)) (not (f27)) (not (f28)) (not (f29)) (not (f30)) (not (f31)) (not (f32)) (not (f33)) (not (f34)) (not (f35)) (not (f36)) (not (f37)) (not (f38)) (not (f39)) (not (f40)) (not (f41)) (not (f42)) (not (f43)) (not (f44)) (not (f45)) (not (f46)) (not (f47)) (not (f48)) (not (f49)) (not (f50)) (not (f51)) (not (f52)) (not (f53)) (not (f54)) (not (f55)) (not (f56)) (not (f57)) (not (f58)) (not (f59)) (not (f60)) (not (f61)) (not (f62)) (not (f63)) (not (f64)) (not (f65)) (not (f66)) (not (f67)) (not (f68)) (not (f69)) (not (f70)) (not (f71)) (not (f72)) (not (f73)) (not (f74)) (not (f75)) (not (f76)) (not (f77)) (not (f78)) (not (f79)) (not (f80)) (not (f81)) (not (f82)) (not (f83)) (not (f84)) (not (f85)) (not (f86)) (not (f87)) (not (f88)) (not (f89)) (not (f90)) (not (f91)) (not (f92)) (not (f93)) (not (f94)) (not (f95)) (not (f96)) (not (f97)) (not (f98)) (not (f99)) (not (f100)) (not (f101)) (not (f102)) (not (f103)) (not (f104)) (not (f105)) (not (f106)) (not (f107)) (not (f108)) (not (f109)) (not (f110)) (not (f111)) (not (f112)) (not (f113)) (not (f114)) (not (f115)) (not (f116)) (not (f117)) (not (f118)) (not (f119)) (not (f120)) (not (f121)) (not (f122)) (not (f123)) (not (f124)) (not (f125)) (not (f126)) (not (f127)) (not (f128)) (not (f129)) (not (f130)) (not (f131)) (not (f132)) (not (f133)) (not (f134)) (not (f135)) (not (f136)) (not (f137)) (not (f138)) (not (f139)) (not (f140)) (not (f141)) (not (f142)) (not (f143)) (not (f144)) (not (f145)) (not (f146)) (not (f147)) (not (f148)) (not (f149)) (not (f150)) (not (f151)) (not (f152)) (not (f153)) (not (f154)) (not (f155)) (not (f156)) (not (f157)) (not (f158))))

    (:action pre-goal
    :precondition (and (f1) (f2))
    :effect (and (f158) (not (f0)) (not (f1)) (not (f2)) (not (f3)) (not (f4)) (not (f5)) (not (f6)) (not (f7)) (not (f8)) (not (f9)) (not (f10)) (not (f11)) (not (f12)) (not (f13)) (not (f14)) (not (f15)) (not (f16)) (not (f17)) (not (f18)) (not (f19)) (not (f20)) (not (f21)) (not (f22)) (not (f23)) (not (f24)) (not (f25)) (not (f26)) (not (f27)) (not (f28)) (not (f29)) (not (f30)) (not (f31)) (not (f32)) (not (f33)) (not (f34)) (not (f35)) (not (f36)) (not (f37)) (not (f38)) (not (f39)) (not (f40)) (not (f41)) (not (f42)) (not (f43)) (not (f44)) (not (f45)) (not (f46)) (not (f47)) (not (f48)) (not (f49)) (not (f50)) (not (f51)) (not (f52)) (not (f53)) (not (f54)) (not (f55)) (not (f56)) (not (f57)) (not (f58)) (not (f59)) (not (f60)) (not (f61)) (not (f62)) (not (f63)) (not (f64)) (not (f65)) (not (f66)) (not (f67)) (not (f68)) (not (f69)) (not (f70)) (not (f71)) (not (f72)) (not (f73)) (not (f74)) (not (f75)) (not (f76)) (not (f77)) (not (f78)) (not (f79)) (not (f80)) (not (f81)) (not (f82)) (not (f83)) (not (f84)) (not (f85)) (not (f86)) (not (f87)) (not (f88)) (not (f89)) (not (f90)) (not (f91)) (not (f92)) (not (f93)) (not (f94)) (not (f95)) (not (f96)) (not (f97)) (not (f98)) (not (f99)) (not (f100)) (not (f101)) (not (f102)) (not (f103)) (not (f104)) (not (f105)) (not (f106)) (not (f107)) (not (f108)) (not (f109)) (not (f110)) (not (f111)) (not (f112)) (not (f113)) (not (f114)) (not (f115)) (not (f116)) (not (f117)) (not (f118)) (not (f119)) (not (f120)) (not (f121)) (not (f122)) (not (f123)) (not (f124)) (not (f125)) (not (f126)) (not (f127)) (not (f128)) (not (f129)) (not (f130)) (not (f131)) (not (f132)) (not (f133)) (not (f134)) (not (f135)) (not (f136)) (not (f137)) (not (f138)) (not (f139)) (not (f140)) (not (f141)) (not (f142)) (not (f143)) (not (f144)) (not (f145)) (not (f146)) (not (f147)) (not (f148)) (not (f149)) (not (f150)) (not (f151)) (not (f152)) (not (f153)) (not (f154)) (not (f155)) (not (f156)) (not (f157))))

    
    (:action add-f0-f1
    :precondition (f0)
    :effect (and (f1)))
        

    (:action add-f1-goal
    :precondition (f1)
    :effect (and (f158) (not (f1))))
        

    (:action add-f0-f2
    :precondition (f0)
    :effect (and (f2)))
        

    (:action add-f2-goal
    :precondition (f2)
    :effect (and (f158) (not (f2))))
        

    (:action add-f0-f3
    :precondition (f0)
    :effect (and (f3) ))
        

    (:action add-f3-f4
    :precondition (f3)
    :effect (and (f4)))
            

    (:action add-f4-f5
    :precondition (f4)
    :effect (and (f5)))
            

    (:action add-f5-f6
    :precondition (f5)
    :effect (and (f6)))
            

    (:action add-f6-f7
    :precondition (f6)
    :effect (and (f7)))
            

    (:action add-f0-f8
    :precondition (f0)
    :effect (and (f8) ))
        

    (:action add-f8-f9
    :precondition (f8)
    :effect (and (f9)))
            

    (:action add-f9-f10
    :precondition (f9)
    :effect (and (f10)))
            

    (:action add-f10-f11
    :precondition (f10)
    :effect (and (f11)))
            

    (:action add-f11-f12
    :precondition (f11)
    :effect (and (f12)))
            

    (:action add-f0-f13
    :precondition (f0)
    :effect (and (f13) ))
        

    (:action add-f13-f14
    :precondition (f13)
    :effect (and (f14)))
            

    (:action add-f14-f15
    :precondition (f14)
    :effect (and (f15)))
            

    (:action add-f15-f16
    :precondition (f15)
    :effect (and (f16)))
            

    (:action add-f16-f17
    :precondition (f16)
    :effect (and (f17)))
            

    (:action add-f0-f18
    :precondition (f0)
    :effect (and (f18) ))
        

    (:action add-f18-f19
    :precondition (f18)
    :effect (and (f19)))
            

    (:action add-f19-f20
    :precondition (f19)
    :effect (and (f20)))
            

    (:action add-f20-f21
    :precondition (f20)
    :effect (and (f21)))
            

    (:action add-f21-f22
    :precondition (f21)
    :effect (and (f22)))
            

    (:action add-f0-f23
    :precondition (f0)
    :effect (and (f23) ))
        

    (:action add-f23-f24
    :precondition (f23)
    :effect (and (f24)))
            

    (:action add-f24-f25
    :precondition (f24)
    :effect (and (f25)))
            

    (:action add-f25-f26
    :precondition (f25)
    :effect (and (f26)))
            

    (:action add-f26-f27
    :precondition (f26)
    :effect (and (f27)))
            

    (:action add-f0-f28
    :precondition (f0)
    :effect (and (f28) ))
        

    (:action add-f28-f29
    :precondition (f28)
    :effect (and (f29)))
            

    (:action add-f29-f30
    :precondition (f29)
    :effect (and (f30)))
            

    (:action add-f30-f31
    :precondition (f30)
    :effect (and (f31)))
            

    (:action add-f31-f32
    :precondition (f31)
    :effect (and (f32)))
            

    (:action add-f0-f33
    :precondition (f0)
    :effect (and (f33) ))
        

    (:action add-f33-f34
    :precondition (f33)
    :effect (and (f34)))
            

    (:action add-f34-f35
    :precondition (f34)
    :effect (and (f35)))
            

    (:action add-f35-f36
    :precondition (f35)
    :effect (and (f36)))
            

    (:action add-f36-f37
    :precondition (f36)
    :effect (and (f37)))
            

    (:action add-f0-f38
    :precondition (f0)
    :effect (and (f38) ))
        

    (:action add-f38-f39
    :precondition (f38)
    :effect (and (f39)))
            

    (:action add-f39-f40
    :precondition (f39)
    :effect (and (f40)))
            

    (:action add-f40-f41
    :precondition (f40)
    :effect (and (f41)))
            

    (:action add-f41-f42
    :precondition (f41)
    :effect (and (f42)))
            

    (:action add-f0-f43
    :precondition (f0)
    :effect (and (f43) ))
        

    (:action add-f43-f44
    :precondition (f43)
    :effect (and (f44)))
            

    (:action add-f44-f45
    :precondition (f44)
    :effect (and (f45)))
            

    (:action add-f45-f46
    :precondition (f45)
    :effect (and (f46)))
            

    (:action add-f46-f47
    :precondition (f46)
    :effect (and (f47)))
            

    (:action add-f0-f48
    :precondition (f0)
    :effect (and (f48) ))
        

    (:action add-f48-f49
    :precondition (f48)
    :effect (and (f49)))
            

    (:action add-f49-f50
    :precondition (f49)
    :effect (and (f50)))
            

    (:action add-f50-f51
    :precondition (f50)
    :effect (and (f51)))
            

    (:action add-f51-f52
    :precondition (f51)
    :effect (and (f52)))
            

    (:action add-f0-f53
    :precondition (f0)
    :effect (and (f53) ))
        

    (:action add-f53-f54
    :precondition (f53)
    :effect (and (f54)))
            

    (:action add-f54-f55
    :precondition (f54)
    :effect (and (f55)))
            

    (:action add-f55-f56
    :precondition (f55)
    :effect (and (f56)))
            

    (:action add-f56-f57
    :precondition (f56)
    :effect (and (f57)))
            

    (:action add-f0-f58
    :precondition (f0)
    :effect (and (f58) ))
        

    (:action add-f58-f59
    :precondition (f58)
    :effect (and (f59)))
            

    (:action add-f59-f60
    :precondition (f59)
    :effect (and (f60)))
            

    (:action add-f60-f61
    :precondition (f60)
    :effect (and (f61)))
            

    (:action add-f61-f62
    :precondition (f61)
    :effect (and (f62)))
            

    (:action add-f0-f63
    :precondition (f0)
    :effect (and (f63) ))
        

    (:action add-f63-f64
    :precondition (f63)
    :effect (and (f64)))
            

    (:action add-f64-f65
    :precondition (f64)
    :effect (and (f65)))
            

    (:action add-f65-f66
    :precondition (f65)
    :effect (and (f66)))
            

    (:action add-f66-f67
    :precondition (f66)
    :effect (and (f67)))
            

    (:action add-f0-f68
    :precondition (f0)
    :effect (and (f68) ))
        

    (:action add-f68-f69
    :precondition (f68)
    :effect (and (f69)))
            

    (:action add-f69-f70
    :precondition (f69)
    :effect (and (f70)))
            

    (:action add-f70-f71
    :precondition (f70)
    :effect (and (f71)))
            

    (:action add-f71-f72
    :precondition (f71)
    :effect (and (f72)))
            

    (:action add-f0-f73
    :precondition (f0)
    :effect (and (f73) ))
        

    (:action add-f73-f74
    :precondition (f73)
    :effect (and (f74)))
            

    (:action add-f74-f75
    :precondition (f74)
    :effect (and (f75)))
            

    (:action add-f75-f76
    :precondition (f75)
    :effect (and (f76)))
            

    (:action add-f76-f77
    :precondition (f76)
    :effect (and (f77)))
            

    (:action add-f0-f78
    :precondition (f0)
    :effect (and (f78) ))
        

    (:action add-f78-f79
    :precondition (f78)
    :effect (and (f79)))
            

    (:action add-f79-f80
    :precondition (f79)
    :effect (and (f80)))
            

    (:action add-f80-f81
    :precondition (f80)
    :effect (and (f81)))
            

    (:action add-f81-f82
    :precondition (f81)
    :effect (and (f82)))
            

    (:action add-f0-f83
    :precondition (f0)
    :effect (and (f83) ))
        

    (:action add-f83-f84
    :precondition (f83)
    :effect (and (f84)))
            

    (:action add-f84-f85
    :precondition (f84)
    :effect (and (f85)))
            

    (:action add-f85-f86
    :precondition (f85)
    :effect (and (f86)))
            

    (:action add-f86-f87
    :precondition (f86)
    :effect (and (f87)))
            

    (:action add-f0-f88
    :precondition (f0)
    :effect (and (f88) ))
        

    (:action add-f88-f89
    :precondition (f88)
    :effect (and (f89)))
            

    (:action add-f89-f90
    :precondition (f89)
    :effect (and (f90)))
            

    (:action add-f90-f91
    :precondition (f90)
    :effect (and (f91)))
            

    (:action add-f91-f92
    :precondition (f91)
    :effect (and (f92)))
            

    (:action add-f0-f93
    :precondition (f0)
    :effect (and (f93) ))
        

    (:action add-f93-f94
    :precondition (f93)
    :effect (and (f94)))
            

    (:action add-f94-f95
    :precondition (f94)
    :effect (and (f95)))
            

    (:action add-f95-f96
    :precondition (f95)
    :effect (and (f96)))
            

    (:action add-f96-f97
    :precondition (f96)
    :effect (and (f97)))
            

    (:action add-f0-f98
    :precondition (f0)
    :effect (and (f98) ))
        

    (:action add-f98-f99
    :precondition (f98)
    :effect (and (f99)))
            

    (:action add-f99-f100
    :precondition (f99)
    :effect (and (f100)))
            

    (:action add-f100-f101
    :precondition (f100)
    :effect (and (f101)))
            

    (:action add-f101-f102
    :precondition (f101)
    :effect (and (f102)))
            

    (:action add-f0-f103
    :precondition (f0)
    :effect (and (f103) ))
        

    (:action add-f103-f104
    :precondition (f103)
    :effect (and (f104)))
            

    (:action add-f104-f105
    :precondition (f104)
    :effect (and (f105)))
            

    (:action add-f105-f106
    :precondition (f105)
    :effect (and (f106)))
            

    (:action add-f106-f107
    :precondition (f106)
    :effect (and (f107)))
            

    (:action add-f0-f108
    :precondition (f0)
    :effect (and (f108) ))
        

    (:action add-f108-f109
    :precondition (f108)
    :effect (and (f109)))
            

    (:action add-f109-f110
    :precondition (f109)
    :effect (and (f110)))
            

    (:action add-f110-f111
    :precondition (f110)
    :effect (and (f111)))
            

    (:action add-f111-f112
    :precondition (f111)
    :effect (and (f112)))
            

    (:action add-f0-f113
    :precondition (f0)
    :effect (and (f113) ))
        

    (:action add-f113-f114
    :precondition (f113)
    :effect (and (f114)))
            

    (:action add-f114-f115
    :precondition (f114)
    :effect (and (f115)))
            

    (:action add-f115-f116
    :precondition (f115)
    :effect (and (f116)))
            

    (:action add-f116-f117
    :precondition (f116)
    :effect (and (f117)))
            

    (:action add-f0-f118
    :precondition (f0)
    :effect (and (f118) ))
        

    (:action add-f118-f119
    :precondition (f118)
    :effect (and (f119)))
            

    (:action add-f119-f120
    :precondition (f119)
    :effect (and (f120)))
            

    (:action add-f120-f121
    :precondition (f120)
    :effect (and (f121)))
            

    (:action add-f121-f122
    :precondition (f121)
    :effect (and (f122)))
            

    (:action add-f0-f123
    :precondition (f0)
    :effect (and (f123) ))
        

    (:action add-f123-f124
    :precondition (f123)
    :effect (and (f124)))
            

    (:action add-f124-f125
    :precondition (f124)
    :effect (and (f125)))
            

    (:action add-f125-f126
    :precondition (f125)
    :effect (and (f126)))
            

    (:action add-f126-f127
    :precondition (f126)
    :effect (and (f127)))
            

    (:action add-f0-f128
    :precondition (f0)
    :effect (and (f128) ))
        

    (:action add-f128-f129
    :precondition (f128)
    :effect (and (f129)))
            

    (:action add-f129-f130
    :precondition (f129)
    :effect (and (f130)))
            

    (:action add-f130-f131
    :precondition (f130)
    :effect (and (f131)))
            

    (:action add-f131-f132
    :precondition (f131)
    :effect (and (f132)))
            

    (:action add-f0-f133
    :precondition (f0)
    :effect (and (f133) ))
        

    (:action add-f133-f134
    :precondition (f133)
    :effect (and (f134)))
            

    (:action add-f134-f135
    :precondition (f134)
    :effect (and (f135)))
            

    (:action add-f135-f136
    :precondition (f135)
    :effect (and (f136)))
            

    (:action add-f136-f137
    :precondition (f136)
    :effect (and (f137)))
            

    (:action add-f0-f138
    :precondition (f0)
    :effect (and (f138) ))
        

    (:action add-f138-f139
    :precondition (f138)
    :effect (and (f139)))
            

    (:action add-f139-f140
    :precondition (f139)
    :effect (and (f140)))
            

    (:action add-f140-f141
    :precondition (f140)
    :effect (and (f141)))
            

    (:action add-f141-f142
    :precondition (f141)
    :effect (and (f142)))
            

    (:action add-f0-f143
    :precondition (f0)
    :effect (and (f143) ))
        

    (:action add-f143-f144
    :precondition (f143)
    :effect (and (f144)))
            

    (:action add-f144-f145
    :precondition (f144)
    :effect (and (f145)))
            

    (:action add-f145-f146
    :precondition (f145)
    :effect (and (f146)))
            

    (:action add-f146-f147
    :precondition (f146)
    :effect (and (f147)))
            

    (:action add-f0-f148
    :precondition (f0)
    :effect (and (f148) ))
        

    (:action add-f148-f149
    :precondition (f148)
    :effect (and (f149)))
            

    (:action add-f149-f150
    :precondition (f149)
    :effect (and (f150)))
            

    (:action add-f150-f151
    :precondition (f150)
    :effect (and (f151)))
            

    (:action add-f151-f152
    :precondition (f151)
    :effect (and (f152)))
            

    (:action add-f0-f153
    :precondition (f0)
    :effect (and (f153) ))
        

    (:action add-f153-f154
    :precondition (f153)
    :effect (and (f154)))
            

    (:action add-f154-f155
    :precondition (f154)
    :effect (and (f155)))
            

    (:action add-f155-f156
    :precondition (f155)
    :effect (and (f156)))
            

    (:action add-f156-f157
    :precondition (f156)
    :effect (and (f157)))
            
    )
    