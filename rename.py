ea = ScreenEA()
streak = []
base = 0

# Iterate functions
for funcea in Functions(SegStart(ea), SegEnd(ea)):
    for (startea, endea) in Chunks(funcea):
        analyzed = 0

        for head in Heads(startea, endea):
            diss = GetDisasm(head)
            analyzed += 1
            
            # Search for a trampoline
            if diss.startswith("ADRP") and len(streak) == 0:
                streak.append(diss)
                base = head
                continue
            
            if diss.startswith("LDR") and len(streak) == 1:
                streak.append(diss)
                continue

            if diss.startswith("BR") and len(streak) == 2:
                if analyzed != 3:
                    continue

                # Once the function has been found find the real function
                adrp_adr = streak[0].split('_')[-1].split('@')[0]

                try:
                    final_adr = GetDisasm(int(adrp_adr, 16)).split(' ')[-1]

                    og_name = GetFunctionName(int(final_adr, 16))
                except ValueError as e:
                    print e, adrp_adr, final_adr

                if og_name.startswith("sub") or 'ADRP' in adrp_adr:
                    continue

                idc.MakeName(base, "%s_%s" %(og_name, adrp_adr))
                streak = []
                print "Renamed trampoline at %x with %s_%s" %(head, og_name, adrp_adr)
                continue
