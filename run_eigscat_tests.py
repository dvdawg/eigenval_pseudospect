import os
import matlab.engine

MATLAB_EIGSCAT_DIR = r""

OUTPUT_DIR = "eigscat_output"
M_DEFAULT = 300  # number of perturbed mats

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_dir_abs = os.path.abspath(OUTPUT_DIR)

    print("Starting MATLAB engine...")
    eng = matlab.engine.start_matlab()
    eng.addpath(MATLAB_EIGSCAT_DIR, nargout=0)
    eng.eval("pause('off');", nargout=0)

    def run_case(case_id: int, a_def: str, err_list, m=M_DEFAULT):
        """Define matrix a in MATLAB, then loop over err values."""
        print(f"\n=== Case {case_id} ===")
        eng.eval(a_def, nargout=0)

        for err in err_list:
            print(f"Case {case_id}, err = {err:g}")
            eng.workspace['m'] = float(m)
            eng.workspace['err'] = float(err)

            out = eng.evalc("eigscat", nargout=1)

            txt_name = f"case{case_id}_err{err:.0e}.txt"
            txt_path = os.path.join(out_dir_abs, txt_name)
            with open(txt_path, "w") as f:
                f.write(out)

            fig_name = f"case{case_id}_err{err:.0e}.png"
            fig_path = os.path.join(out_dir_abs, fig_name)
            fig_path_mat = fig_path.replace("\\", "/")
            eng.eval(f"saveas(gcf, '{fig_path_mat}')", nargout=0)


    case1_a = r"""
        a = randn(5);
        while all(imag(eig(a)) == 0)
            a = randn(5);
        end
    """
    case1_err = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 2e-1]
    run_case(1, case1_a, case1_err)

    case2_a = r"a = diag(ones(4,1),1);"
    case2_err = [1e-12, 1e-10, 1e-8]
    run_case(2, case2_a, case2_err)

    case3_a = r"""
        a = [1  1e6   0   0;
             0   2  1e-3 0;
             0   0   3  10;
             0   0  -1   4];
    """
    case3_err = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
    run_case(3, case3_a, case3_err)

    case4_a = r"""
        [q,r] = qr(randn(4,4));
        a = q*diag(ones(3,1),1)*q';
    """
    case4_err = [1e-16, 1e-14, 1e-12, 1e-10, 1e-8]
    run_case(4, case4_a, case4_err)

    case5_a = r"""
        a = [1  1e3 1e6;
             0   1  1e3;
             0   0   1];
    """
    case5_err = [1e-7, 1e-6, 5e-6, 8e-6, 1e-5, 1.5e-5, 2e-5]
    run_case(5, case5_a, case5_err)

    case6_a = r"""
        a = [1  0   0   0    0    0;
             0  2   1   0    0    0;
             0  0   2   0    0    0;
             0  0   0   3   1e2  1e4;
             0  0   0   0    3   1e2;
             0  0   0   0    0    3];
    """
    case6_err = [1e-10, 1e-8, 1e-6, 1e-4, 1e-3]
    run_case(6, case6_a, case6_err)

    eng.quit()


if __name__ == "__main__":
    main()
