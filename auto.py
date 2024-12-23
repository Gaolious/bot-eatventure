from auto_pre import AutoHelper as PreAuto
from auto_scan import AutoHelper as ScanAuto

package_name = "com.hwqgrhhjfd.idlefastfood"
if __name__ == '__main__':
    curr = 0

    for i in range(200):
        curr = curr + 1
        print(f'Current Run : {curr} - Pre-defined Position Auto')
        try:
            helper = PreAuto(package_name)
            helper.run()
        except Exception as e:
            print(e)

        curr = curr + 1
        print(f'Current Run : {curr} - Scan Auto')
        try:
            helper = ScanAuto(package_name)
            helper.run()
        except Exception as e:
            print(e)
